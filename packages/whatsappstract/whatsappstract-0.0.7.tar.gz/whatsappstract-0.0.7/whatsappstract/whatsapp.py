import logging
import re
import time
from typing import Iterable, List, Set, Optional
from urllib.parse import parse_qs
from urllib.parse import urlparse
import dateparser 
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException, StaleElementReferenceException, \
    TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait


class Whatsapp():
    '''A WhatsApp scraper without a proper docstring'''

    def __init__(self, geckopath=None, screenshot_folder=None, days=None):
        opts = dict(executable_path=geckopath) if geckopath else {}
        self.screenshot_folder = screenshot_folder
        self.scraped_names: Set[str] = set()
        self.days = days
        try:
            self.browser = webdriver.Firefox(**opts)
        except WebDriverException:
            logging.error("Geckodriver not found. Either copy the geckodriver to your path or specify its location")
            raise
        self.browser.get("https://web.whatsapp.com/")

    def get_qr(self) -> str:
        # If there is a "click to refresh QR code" message, click it
        clickme = self.browser.find_elements_by_css_selector("[aria-label='Scan me!']")
        if clickme:
            try:
                clickme[0].click()
            except ElementClickInterceptedException:
                pass

        c = WebDriverWait(self.browser, 5).until(
            presence_of_element_located((By.CSS_SELECTOR, "canvas"))
        )
        return c.screenshot_as_base64

    def is_qr_scanned(self):
        try:
            self.browser.find_element_by_xpath('//h1')
            return True
        except NoSuchElementException:
            return False

    def wait_to_be_ready(self):
        while True:
            if self.is_qr_scanned():
                time.sleep(1)
                return
            else:
                logging.info("Seems that WhatsApp is not ready yet, wait for a second...")
                time.sleep(1)

    def get_visible_chats(self) -> Iterable[WebElement]:
        """
        Yield a name item pair for the chats currently on the screen in the left pane,
        ordered from top
        """
        a = self.browser.find_elements_by_xpath("//div[@id='pane-side']//span[@title and @dir='auto']")
        chats = []
        for item in a:
            try:
                chats.append((item.location['y'], item))
            except StaleElementReferenceException:
                logging.info(f"Skipping stale reference {item}")
                continue  # not sure why this happens, but it does
        return [chat for _, chat in sorted(chats)]

    def get_next_chat(self) -> Optional[WebElement]:
        logging.info("Finding the next chat...")
        scroll = None
        while True:
            chats = self.get_visible_chats()
            if not chats:
                raise Exception("No chats available?")
            new_chats = [c for c in chats if not c.text in self.scraped_names]
            if new_chats:
                self.scraped_names.add(new_chats[0].text)
                return new_chats[0]
            logging.info("Scrolling to next chat page")
            if chats[-1] == scroll:
                logging.info("Scrolling did not change list - done?")
                return None
            scroll = chats[-1]
            self.browser.execute_script("arguments[0].scrollIntoView();", scroll)
            time.sleep(1)  # Allow scroll to execute

    def get_all_chats(self) -> Iterable[WebElement]:
        """Yield items for all chats (scrolling down when needed), ordered from top"""
        while True:
            try:
                next_chat = self.get_next_chat()
                if next_chat:
                    yield next_chat
                else:
                    break
            except StaleElementReferenceException:
                logging.info("Stale reference on getting chat, sleeping one second and retrying")
                time.sleep(1)
                continue

    def _screenshot(self, name="") -> str:
        """
        If configured, take a screenshot and return a "(screenshot saved as 'fn')" text.
        Otherwise, return empty string
        """
        if not self.screenshot_folder:
            return ""
        fn = f"{self.screenshot_folder}/screenshot_{name}_{hash(self)}.png"
        self.browser.save_screenshot(fn)
        return f"(Screenshot saved as {fn})"

    def open_links_pane(self):
        """Open the links (in the media, links, docs) pane for the currently open chat"""
        # Find the avatar button to get media link
        try:
            x = self.browser.find_element_by_xpath("//div[@id = 'main']/header/div/div/img")
        except NoSuchElementException:
            x = self.browser.find_element_by_xpath("//div[@id = 'main']/header//*[@dir = 'auto']")
        x.click()
        time.sleep(5)
        txt = self._screenshot("open_medialink_pre")
        if txt:
            print(txt)
            logging.info(txt)
        # Find the right link for getting the links
        media_link = None
        for linktext in [
            "Medien, Links und Dokumente",
            "Media, links en documenten",
            "Media, Links and Docs"]:
            try:
                xpath = f"//span[text() = '{linktext}']"
                media_link = self.browser.find_element_by_xpath(xpath)
            except NoSuchElementException:
                continue
        if media_link is None:
            txt = self._screenshot("open_medialink")
            raise Exception(f"Cannot find 'media, links and docs' link {txt}")
        media_link.click()
        xpath = "//*[text() = 'Links']"
        WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        # Click on the 'links' tab
        linktext2 = self.browser.find_element_by_xpath(xpath)
        linktext2.click()
        time.sleep(5)

    def get_all_links(self) -> Iterable[WebElement]:
        """Yield all links (<a> elements) in the list of links, scrolling down if needed"""
        seen = set()
        n = 0
        while True:
            last_link = None
            for link in self.browser.find_elements_by_xpath(
                "//*[@data-list-scroll-container = 'true']"
                "//*[contains(@class,'message-in') or contains(@class,'message-out')]"):
                if link in seen:
                    continue
                seen.add(link)
                last_link = link
                yield link
            if last_link is None:
                n += 1
                if n < 2:
                    time.sleep(5)
                    continue
                break
            self.browser.execute_script("arguments[0].scrollIntoView();", last_link)

    def scrape_link(self, link: WebElement) -> dict:
        """
        Scrape a single link from the links pane, returning a dict with uri, direction, sender, and date
        """
        result = dict(uri = link.find_element_by_xpath(".//a").get_attribute("href"))
        dir_class = link.get_attribute("class")
        if "message-in" in dir_class:
            result['direction'] = "received"
        elif "message-out" in dir_class:
            result['direction'] = "sent"
        else:
            raise ValueError(f"Unknown dir_class: {dir_class}")
        try:
            #Get the date from the links pane
            x = link.find_element_by_xpath(".//div[contains(@class,'copyable-text')]")
            preplaintext = x.get_attribute("data-pre-plain-text")
            m = re.match(r"\[(.*?)\] (.*):", preplaintext)
            if not m:
                raise ValueError(f"Cannot parse preplaintext: {preplaintext}")
            result['date'] = m.group(1)
            result['sender'] = m.group(2)
        except NoSuchElementException:
            #Alternative: click on link to scroll to chat and get the date from the chat
            try:
                x = link.find_element_by_xpath(".//div[span[@data-icon='tail-in']]")
                x.click()
                xpath = "//div[contains(@class, 'focusable-list-item')]//a[@href = '"+result['uri']+"']"
                WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                cm = self.browser.find_element_by_xpath(xpath)
                preplaintext = cm.find_element_by_xpath(
                    "ancestor::div[@data-pre-plain-text]").get_attribute("data-pre-plain-text")
                m = re.match(r"\[(.*?)\] (.*):", preplaintext)
                if not m:
                    raise ValueError(f"Cannot parse preplaintext: {preplaintext}")
                result['date'] = m.group(1)
                result['sender'] = m.group(2)
            except (NoSuchElementException, TimeoutException):
                #At the moment still fails if several links were sent in the same message
                logging.warning(f"Cannot get metadata for {result['uri']}")
        return result
    
    def check_date(self, link: dict) -> bool: 
        """
        Check whether the date of a link is too far in the past (default: 90 days).
        Stops scraping if this is the case.
        """
        try:
            parsed = dateparser.parse(link['date'], settings={'DATE_ORDER': 'DMY'})
            diff = datetime.now() - parsed
            if diff.days > self.days:
                return False
            else:
                return True
        except:
            return True

    def get_links_per_chat(self, item: WebElement) -> Iterable[dict]:
        """
        Get all links in a chat (contact).
        :param item should be the WebElement representing the contact's name
        """
        chatname = item.text
        item.click()  # Open this chat
        self.open_links_pane()
        for link in self.get_all_links():
            result = self.scrape_link(link)
            result['chatname'] = chatname
            yield result
            if self.check_date(result) is False:
                break

    def scrape_links(self) -> Iterable[List[dict]]:
        '''
        Yields the *links* per chat that are shared in the Whatsapp scraper instance
        For each chat, yield list of dicts with keys direction, link, name, date
        '''
        self.wait_to_be_ready()
        for name, chat in self.get_all_chats():
            yield list(self.get_links_per_chat(chat))


    def quit_browser(self):
        self.browser.quit()

    def blur(self):
        self.browser.execute_script("document.getElementsByTagName('body')[0].style.filter = 'blur(30px)';")


def anonymize_url(link, origin):
    base = urlparse(link)
    stripped_link = base.scheme + '://' + base.netloc + base.path
    queries = parse_qs(base.query)
    # Get search queries from search engines (Google, Bing, Yahoo, DuckDuckGo, Ecosia), Youtube and large Dutch media providers
    queries_keep = {k: v for k, v in queries.items() if k in ['v', 'q', 'p', 's', 'query', 'keyword', 'term']}
    return ({"link": stripped_link, "query": queries_keep})

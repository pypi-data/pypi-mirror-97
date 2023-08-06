import json

def _to_str(i):
    if type(i) is str:
        return i
    elif type(i) is list:
        return "".join([str(e) for e in i])
    elif type(i) is dict:
        return str(i)

def _links_from_message(message, keep_link = ("link", "query"), keep_message = ("sender", "text")):
    '''
    takes a whatsapp message and returns sanitized links
    keep_link: fields to keep on the link level
    keep_message: fields to keep on the message level
    '''
    
    link = message['link']

    sanitized_link = {k: _to_str(link.get(k,"")) for k in keep_link}
    sanitized_link.update({k: _to_str(message.get(k,"")) for k in keep_message})

    return sanitized_link

def _flatten_chatlinks(chat):
    chatname = chat.get('chatname',"")
    timestamp = chat.get('date',"")
    inlinks = [_links_from_message(message) for message in chat['messages_in']]
    outlinks = [_links_from_message(message) for message in chat['messages_out']]
    for link in inlinks:
        yield {"direction": "received",
               "link": link,
               "chatname": chatname,
               "date": timestamp}

    for link in outlinks:
        yield {"direction": "send",
               "link": link,
               "chatname": chatname,
               "date": timestamp}


        
def jsonlines_to_osd2f(fnin, fnout):
    '''Returns a (temporary) jsonlines file with scraped data and writes a sanitized json file that is compatabile with the OSD2F Data Donation Framework'''
    with open(fnin) as fi, open(fnout, mode='w') as fo:
        data = [json.loads(line) for line in fi]
        json.dump([e for chat in data for e in _flatten_chatlinks(chat)], fo)

            

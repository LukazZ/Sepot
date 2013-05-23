'''
Created on 21.5.2013

@author: lukas.novak.ext

small avail functions
'''

def addtext(TV,text,clear_first):
    '''
    Adds new line of text into TextViewer object     
    :param TV: TextView widget
    :param text: String to be added
    :param clear_first: Erase current content before adding text
    '''
    atbuffer = TV.get_buffer()
    atiter = atbuffer.get_iter_at_mark(atbuffer.get_insert())
    if clear_first:
        atbuffer.set_text("")
        print "textbuffer is emptied"
    atbuffer.insert(atiter,"%s\n"%text)   # use "\n" for newlines        

# if __name__ == '__main__':
#     pass
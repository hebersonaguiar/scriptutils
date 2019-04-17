from pyotrs import Client, Article, Ticket
client = Client("http://172.16.1.50", "admin", "admin")
client.session_create()
#client.ticket_get_by_id(2, articles=True, attachments=False, dynamic_fields=False)
new_ticket = Ticket.create_basic(Title="This is the Title",
                                     Queue="Junk",
                                     State=u"new",
                                     Priority=u"3 normal",
                                     CustomerUser="test")
first_article = Article({"Subject": "Subj", "Body": "New Body"})
client.ticket_create(new_ticket, first_article)


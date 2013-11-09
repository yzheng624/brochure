from django.core.mail import send_mail as _send_mail


def send_mail(product, to_list):
    # content = 'Type: ' + product.type + '\n'
    content = ''
    content += 'Item: ' + product.name + '\n'
    content += 'Sku: ' + product.uuid + '\n'
    content += 'Current Price: ' + str(product.current_price) + '\n'
    content += 'Reason: Price Drop\n'
    content += 'Item Link: ' + product.url + '\n'
    content += 'Amazon Link: ' \
               + 'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=' \
               + product.name
    _send_mail(product.name + '\'s price been updated', content,
              'brochuredev@126.com', to_list, fail_silently=False)
    print content
    print to_list
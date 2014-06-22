from django import template

register = template.Library()


@register.filter
def slice_pages(pages, delta=5):
    '''
    Slices the pages in an endless paginator to return a maximum of 5
    elements on each side.

    :param pages: A PageList, that can be iterated on.
    :returns: A list of pages, where the resulting pages are the ones to be
              shown to the user.
    '''
    first_index = max(0, pages.current().number - delta)
    last_index = min(len(pages), pages.current().number + delta)
    return [e for e in pages][first_index:last_index]

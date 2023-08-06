from pi_touch_gui import Page


def get_pages():
    from test_pages.entry_page import entry_page
    from test_pages.poweroff_page import poweroff_page
    from test_pages.sampler_page import sampler_page

    return [entry_page(), sampler_page(Page.LCARS), poweroff_page()]

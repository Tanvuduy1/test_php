# -*- coding: utf-8 -*-
import sys
import os
import json
import time

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from playwright.sync_api import sync_playwright

CDP_URL = "http://localhost:9222"

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(CDP_URL)
    context = browser.contexts[0]
    page = [pg for pg in context.pages if "midesk" in pg.url][0]
    tf = page.frame("gidindexTicketFrame")
    
    captured = []
    def on_res(res):
        if any(res.url.endswith(ext) for ext in ['.js', '.css', '.png', '.jpg', '.ico']):
            return
        if res.request.resource_type in ['fetch', 'xhr']:
            captured.append(res.url)
            
    page.on("response", on_res)
    
    print("Testing DataTables Pagination...")
    captured.clear()
    tf.evaluate("""() => {
        // Switch to page 2 (index 1)
        $('#table_ticket').DataTable().page(1).draw('page');
    }""")
    page.wait_for_timeout(4000)
    print("Pagination Triggered Requests:", len(captured))
    for u in captured:
        print(" ", u)

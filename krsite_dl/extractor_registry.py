# krsite_dl/extractor_registry.py
# REVISED - This file now enables true lazy loading.

"""
Module: extractor_registry.py
Author: danrynr

Description:
This module provides a lightweight dictionary that maps a unique hostname
(or part of a hostname) to the import path of the module that handles it.

This allows the main application to load instantly and only import the
specific extractor module needed for a given URL, greatly improving startup speed.
"""

LAZY_EXTRACTOR_MAP = {
    # Frequent Sites
    'blog.naver.com': 'krsite_dl.extractor.naverblog',
    'programs.sbs.co.kr': 'krsite_dl.extractor.sbs',
    'sbskpop.kr': 'krsite_dl.extractor.sbskpop',
    'news.sbs.co.kr': 'krsite_dl.extractor.sbsnews',
    'entertain.naver.com': 'krsite_dl.extractor.naverenter',
    'news.naver.com': 'krsite_dl.extractor.navernews',
    'post.naver.com': 'krsite_dl.extractor.naverpost',
    'mbc.co.kr': 'krsite_dl.extractor.mbc',
    'melon.com': 'krsite_dl.extractor.melon',

    # KR
    'cosmopolitan.co.kr': 'krsite_dl.extractor.cosmopolitan',
    'dazedkorea.com': 'krsite_dl.extractor.dazedkorea',
    'dispatch.co.kr': 'krsite_dl.extractor.dispatch',
    'elle.co.kr': 'krsite_dl.extractor.elle',
    'esquirekorea.co.kr': 'krsite_dl.extractor.esquire',
    'genie.co.kr': 'krsite_dl.extractor.genie',
    'harpersbazaar.co.kr': 'krsite_dl.extractor.harpersbazaar',
    'isplus.com': 'krsite_dl.extractor.ilgansports', # For Ilgan Sports
    'imnews.imbc.com': 'krsite_dl.extractor.imbcnews',
    'k-odyssey.com': 'krsite_dl.extractor.kodyssey',
    'lofficielkorea.com': 'krsite_dl.extractor.lofficielkorea',
    'marieclairekorea.com': 'krsite_dl.extractor.marieclairekorea',
    'news1.kr': 'krsite_dl.extractor.news1',
    'newsen.com': 'krsite_dl.extractor.newsen',
    'newsjamm.kr': 'krsite_dl.extractor.newsjamm',
    'osen.co.kr': 'krsite_dl.extractor.osen',
    'sportsw.kr': 'krsite_dl.extractor.sportsw',
    'tistory.com': 'krsite_dl.extractor.tistory',
    'topstarnews.net': 'krsite_dl.extractor.topstarnews',
    'tv.jtbc.co.kr': 'krsite_dl.extractor.tvjtbc',
    'tvreport.co.kr': 'krsite_dl.extractor.tvreport',
    'vogue.co.kr': 'krsite_dl.extractor.vogue',
    'wkorea.com': 'krsite_dl.extractor.wkorea',

    # JP
    'mikantimes.com': 'krsite_dl.extractor.mikantimes',
    'natalie.mu': 'krsite_dl.extractor.nataliemu',
    'nonno.hpplus.jp': 'krsite_dl.extractor.nonno',
    'spur.hpplus.jp': 'krsite_dl.extractor.spurjp',
    'vivi.tv': 'krsite_dl.extractor.vivi',

    # SG
    'lofficielsingapore.com': 'krsite_dl.extractor.lofficielsingapore',
}

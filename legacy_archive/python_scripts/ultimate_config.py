"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║   ██████╗ ███████╗███╗   ███╗██████╗ ██╗     ███████╗                  ║
║   ██╔══██╗██╔════╝████╗ ████║██╔══██╗██║     ██╔════╝                  ║
║   ██████╔╝█████╗  ██╔████╔██║██████╔╝██║     █████╗                    ║
║   ██╔══██╗██╔══╝  ██║╚██╔╝██║██╔═══╝ ██║     ██╔══╝                    ║
║   ██║  ██║███████╗██║ ╚═╝ ██║██║     ███████╗███████╗                  ║
║   ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═╝     ╚══════╝╚══════╝                  ║
║                                                                            ║
║   ██████╗ ███████╗███████╗ ██████╗██╗   ██╗███████╗                    ║
║   ██╔══██╗██╔════╝██╔════╝██╔════╝██║   ██║██╔════╝                    ║
║   ██████╔╝█████╗  ███████╗██║     ██║   ██║█████╗                      ║
║   ██╔══██╗██╔══╝  ╚════██║██║     ██║   ██║██╔══╝                      ║
║   ██║  ██║███████╗███████║╚██████╗╚██████╔╝███████╗                    ║
║   ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚══════╝                    ║
║                                                                            ║
║   ███╗   ███╗ █████╗ ██╗     ███████╗███╗   ███╗ █████╗ ██╗   ██╗███████╗ ║
║   ████╗ ████║██╔══██╗██║     ██╔════╝████╗ ████║██╔══██╗██║   ██║██╔════╝ ║
║   ██╔████╔██║███████║██║     █████╗  ██╔████╔██║███████║██║   ██║███████╗ ║
║   ██║╚██╔╝██║██╔══██║██║     ██╔══╝  ██║╚██╔╝██║██╔══██║██║   ██║╚════██║ ║
║   ██║ ╚═╝ ██║██║  ██║███████╗███████╗██║ ╚═╝ ██║██║  ██║╚██████╔╝███████║ ║
║   ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝ ║
║                                                                            ║
║                 💼 SAM CORDASHI - HR & OPERATIONS 💼                      ║
║                                                                            ║
║              ULTIMATE SUPER HYPER MAXIMUM POWER ENGINE                      ║
║                                                                            ║
║   ✓ 195 Countries Worldwide    ✓ 50+ Job Platforms                        ║
║   ✓ 100+ Email Patterns      ✓ 15+ SMTP Providers                       ║
║   ✓ AI-Powered Matching      ✓ Auto-Retry & Self-Healing               ║
║   ✓ Telegram Dashboard       ✓ Real-Time Monitoring                     ║
║   ✓ Multi-Language Support   ✓ Anti-Detection                          ║
║                                                                            ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import random
import json
import re
import hashlib
import base64
import sqlite3
import threading
import asyncio
import logging
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
from collections import deque

# ============================================================================
# ULTIMATE CONFIGURATION - MAXIMUM POWER
# ============================================================================

@dataclass
class UltimateConfig:
    """MAXIMUM CONFIGURATION - EVERYTHING ENABLED"""
    
    # ULTRA PERFORMANCE
    MAX_ACCOUNTS_PER_DAY: int = 100
    MAX_APPLICATIONS_PER_DAY: int = 1000
    MAX_EMAILS_PER_HOUR: int = 500
    MAX_PROXY_ROTATIONS: int = 200
    MAX_PARALLEL_THREADS: int = 20
    
    # SMTP PROVIDERS (15+)
    SMTP_PROVIDERS: List[Dict] = field(default_factory=lambda: [
        {"name": "Brevo", "host": "smtp-relay.brevo.com", "port": 587, "user": os.getenv("BREVO_SMTP_LOGIN", ""), "pass": os.getenv("BREVO_SMTP_PASSWORD", "")},
        {"name": "Gmail", "host": "smtp.gmail.com", "port": 587, "user": os.getenv("GMAIL_SMTP_USER", ""), "pass": os.getenv("GMAIL_APP_PASSWORD", "")},
        {"name": "Outlook", "host": "smtp-mail.outlook.com", "port": 587, "user": os.getenv("OUTLOOK_USER", ""), "pass": os.getenv("OUTLOOK_PASSWORD", "")},
        {"name": "Yahoo", "host": "smtp.mail.yahoo.com", "port": 587, "user": "", "pass": ""},
        {"name": "Zoho", "host": "smtp.zoho.com", "port": 587, "user": "", "pass": ""},
        {"name": "Mailgun", "host": "smtp.mailgun.org", "port": 587, "user": "", "pass": ""},
        {"name": "SendGrid", "host": "smtp.sendgrid.net", "port": 587, "user": "apikey", "pass": os.getenv("SENDGRID_API_KEY", "")},
        {"name": "Amazon SES", "host": "email-smtp.us-east-1.amazonaws.com", "port": 587, "user": os.getenv("AWS_ACCESS_KEY", ""), "pass": os.getenv("AWS_SECRET_KEY", "")},
        {"name": "Mailjet", "host": "in-v3.mailjet.com", "port": 587, "user": "", "pass": ""},
        {"name": "Postmark", "host": "smtp.postmarkapp.com", "port": 587, "user": "", "pass": ""},
        {"name": "SocketLabs", "host": "smtp.socketlabs.com", "port": 587, "user": "", "pass": ""},
        {"name": "FastMail", "host": "smtp.fastmail.com", "port": 587, "user": "", "pass": ""},
        {"name": "Namecheap", "host": "smtp.namecheap.com", "port": 587, "user": "", "pass": ""},
        {"name": "GoDaddy", "host": "smtpout.secureserver.net", "port": 587, "user": "", "pass": ""},
        {"name": "ServerPile", "host": "mail.serverpile.com", "port": 587, "user": "", "pass": ""},
    ])
    
    # USER AGENTS (50+ for anti-detection)
    USER_AGENTS: List[str] = field(default_factory=lambda: [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    ])
    
    # COUNTRIES (195 Countries)
    COUNTRIES: List[Dict] = field(default_factory=lambda: [
        # ===== EUROPE (50) =====
        {"code": "GB", "name": "United Kingdom", "lang": "en", "currency": "GBP", "jobs_url": "indeed.co.uk,linkedin.com,cv-library.co.uk,reed.co.uk,jobs.ac.uk"},
        {"code": "DE", "name": "Germany", "lang": "de", "currency": "EUR", "jobs_url": "indeed.de,linkedin.com,stepstone.de,arbeitsagentur.de,stellenanzeigen.de"},
        {"code": "FR", "name": "France", "lang": "fr", "currency": "EUR", "jobs_url": "indeed.fr,linkedin.com,pole-emploi.fr,apec.fr,keljob.com"},
        {"code": "ES", "name": "Spain", "lang": "es", "currency": "EUR", "jobs_url": "indeed.es,linkedin.com,infojobs.net,trabajo.org,neuronita.es"},
        {"code": "IT", "name": "Italy", "lang": "it", "currency": "EUR", "jobs_url": "indeed.it,linkedin.com,infojobs.it,lavoro.org,careerjet.it"},
        {"code": "NL", "name": "Netherlands", "lang": "nl", "currency": "EUR", "jobs_url": "indeed.nl,linkedin.com,intermediair.nl,ictjob.nl,vacatures.nl"},
        {"code": "BE", "name": "Belgium", "lang": "nl", "currency": "EUR", "jobs_url": "indeed.be,linkedin.com,vdab.be,jobat.be,careerjet.be"},
        {"code": "CH", "name": "Switzerland", "lang": "de", "currency": "CHF", "jobs_url": "indeed.ch,linkedin.com,jobs.ch,ictjobs.ch,glassdoor.ch"},
        {"code": "AT", "name": "Austria", "lang": "de", "currency": "EUR", "jobs_url": "indeed.at,linkedin.com,jobs.at,karriere.at,glassdoor.at"},
        {"code": "PL", "name": "Poland", "lang": "pl", "currency": "PLN", "jobs_url": "indeed.pl,linkedin.com,pracuj.pl,goldman.pl,glassdoor.pl"},
        {"code": "SE", "name": "Sweden", "lang": "sv", "currency": "SEK", "jobs_url": "indeed.se,linkedin.com,arbetsformedlingen.se,jobbsafari.se,glassdoor.se"},
        {"code": "NO", "name": "Norway", "lang": "no", "currency": "NOK", "jobs_url": "indeed.no,linkedin.com,finn.no,jobbnorge.no,glassdoor.no"},
        {"code": "DK", "name": "Denmark", "lang": "da", "currency": "DKK", "jobs_url": "indeed.dk,linkedin.com,jobindex.dk,jobsindenmark.dk,glassdoor.dk"},
        {"code": "FI", "name": "Finland", "lang": "fi", "currency": "EUR", "jobs_url": "indeed.fi,linkedin.com,te-palvelut.fi,tyomarkkinatori.fi,glassdoor.fi"},
        {"code": "IE", "name": "Ireland", "lang": "en", "currency": "EUR", "jobs_url": "indeed.ie,linkedin.com,irishjobs.ie,jobs.ie,glassdoor.ie"},
        {"code": "PT", "name": "Portugal", "lang": "pt", "currency": "EUR", "jobs_url": "indeed.pt,linkedin.com,empregosonline.pt,net-empregos.com,glassdoor.pt"},
        {"code": "GR", "name": "Greece", "lang": "el", "currency": "EUR", "jobs_url": "indeed.gr,linkedin.com,career.gr,jobs.gr,glassdoor.gr"},
        {"code": "CZ", "name": "Czech Republic", "lang": "cs", "currency": "CZK", "jobs_url": "indeed.cz,linkedin.com,jobs.cz,prace.cz,glassdoor.cz"},
        {"code": "HU", "name": "Hungary", "lang": "hu", "currency": "HUF", "jobs_url": "indeed.hu,linkedin.com,profession.hu,jobline.hu,glassdoor.hu"},
        {"code": "RO", "name": "Romania", "lang": "ro", "currency": "RON", "jobs_url": "indeed.ro,linkedin.com,ejobs.ro,bestjobs.ro,glassdoor.ro"},
        {"code": "BG", "name": "Bulgaria", "lang": "bg", "currency": "BGN", "jobs_url": "indeed.bg,linkedin.com,jobs.bg,zaplata.bg,glassdoor.bg"},
        {"code": "HR", "name": "Croatia", "lang": "hr", "currency": "EUR", "jobs_url": "indeed.hr,linkedin.com,burzarad.hr,posao.hr,glassdoor.hr"},
        {"code": "SK", "name": "Slovakia", "lang": "sk", "currency": "EUR", "jobs_url": "indeed.sk,linkedin.com,profesia.sk,kariéry.sk,glassdoor.sk"},
        {"code": "SI", "name": "Slovenia", "lang": "sl", "currency": "EUR", "jobs_url": "indeed.si,linkedin.com,mojedelo.com,career.si,glassdoor.si"},
        {"code": "LT", "name": "Lithuania", "lang": "lt", "currency": "EUR", "jobs_url": "indeed.lt,linkedin.com,cvbankas.lt,cv.lt,glassdoor.lt"},
        {"code": "LV", "name": "Latvia", "lang": "lv", "currency": "EUR", "jobs_url": "indeed.lv,linkedin.com,cv.lv,darba.lv,glassdoor.lv"},
        {"code": "EE", "name": "Estonia", "lang": "et", "currency": "EUR", "jobs_url": "indeed.ee,linkedin.com,cv.ee,too.ee,glassdoor.ee"},
        {"code": "UA", "name": "Ukraine", "lang": "uk", "currency": "UAH", "jobs_url": "indeed.ua,linkedin.com,work.ua,hh.ua,robota.ua"},
        {"code": "RS", "name": "Serbia", "lang": "sr", "currency": "RSD", "jobs_url": "indeed.rs,linkedin.com,poslovi.rs,kurir.rs,glassdoor.rs"},
        {"code": "BA", "name": "Bosnia", "lang": "bs", "currency": "BAM", "jobs_url": "indeed.ba,linkedin.com,radnicka-agencija.ba,sw.ba,glassdoor.ba"},
        {"code": "AL", "name": "Albania", "lang": "sq", "currency": "ALL", "jobs_url": "indeed.al,linkedin.com,puna.al,careeralerts.al,glassdoor.al"},
        {"code": "MK", "name": "North Macedonia", "lang": "mk", "currency": "MKD", "jobs_url": "indeed.mk,linkedin.com,career.mk,potencijal.mk,glassdoor.mk"},
        {"code": "ME", "name": "Montenegro", "lang": "me", "currency": "EUR", "jobs_url": "indeed.me,linkedin.com,eures.ec.europa.eu,radnik.me,glassdoor.me"},
        {"code": "XK", "name": "Kosovo", "lang": "sq", "currency": "EUR", "jobs_url": "indeed.xk,linkedin.com,careersinkosovo.com,perputhen.com,glassdoor.xk"},
        {"code": "IS", "name": "Iceland", "lang": "is", "currency": "ISK", "jobs_url": "indeed.is,linkedin.com,job.is,bls.is,glassdoor.is"},
        {"code": "LU", "name": "Luxembourg", "lang": "fr", "currency": "EUR", "jobs_url": "indeed.lu,linkedin.com,jobs.lu,career.lu,glassdoor.lu"},
        {"code": "MT", "name": "Malta", "lang": "mt", "currency": "EUR", "jobs_url": "indeed.mt,linkedin.com,careersinmalta.com,maltapost.com,glassdoor.mt"},
        {"code": "CY", "name": "Cyprus", "lang": "el", "currency": "EUR", "jobs_url": "indeed.cy,linkedin.com,careerfind.com.cy,cyprusjobs.com,glassdoor.cy"},
        {"code": "GB", "name": "Scotland", "lang": "en", "currency": "GBP", "jobs_url": "indeed.co.uk,linkedin.com,scotjobs.co.uk,strath.ac.uk,glassdoor.co.uk"},
        {"code": "GB", "name": "Wales", "lang": "en", "currency": "GBP", "jobs_url": "indeed.co.uk,linkedin.com,welshjobs.co.uk,cardiff.ac.uk,glassdoor.co.uk"},
        {"code": "GB", "name": "Northern Ireland", "lang": "en", "currency": "GBP", "jobs_url": "indeed.co.uk,linkedin.com,nijobs.com,belfast.ac.uk,glassdoor.co.uk"},
        
        # ===== NORTH AMERICA (25) =====
        {"code": "US", "name": "United States", "lang": "en", "currency": "USD", "jobs_url": "indeed.com,linkedin.com,ziprecruiter.com,glassdoor.com,monster.com,careerbuilder.com,simplyhired.com,snagajob.com"},
        {"code": "CA", "name": "Canada", "lang": "en", "currency": "CAD", "jobs_url": "indeed.ca,linkedin.com,eluta.ca,workopolis.com,monster.ca,glassdoor.ca,careerbuilder.ca"},
        {"code": "MX", "name": "Mexico", "lang": "es", "currency": "MXN", "jobs_url": "indeed.com.mx,linkedin.com,computrabajo.com,bumeran.com,occ.com.mx,glassdoor.mx"},
        {"code": "GT", "name": "Guatemala", "lang": "es", "currency": "GTQ", "jobs_url": "indeed.gt,linkedin.com,computrabajo.com,occ.com.gt,glassdoor.gt"},
        {"code": "BZ", "name": "Belize", "lang": "en", "currency": "BZD", "jobs_url": "indeed.bz,linkedin.com,caribbeanjobs.com,belizejobs.com,glassdoor.bz"},
        {"code": "HN", "name": "Honduras", "lang": "es", "currency": "HNL", "jobs_url": "indeed.hn,linkedin.com,computrabajo.com,hondurasjobs.com,glassdoor.hn"},
        {"code": "SV", "name": "El Salvador", "lang": "es", "currency": "USD", "jobs_url": "indeed.com.sv,linkedin.com,computrabajo.com,elsalvadorjobs.com,glassdoor.sv"},
        {"code": "NI", "name": "Nicaragua", "lang": "es", "currency": "NIO", "jobs_url": "indeed.ni,linkedin.com,nicaraguajob.com,nicaraguaocc.com,glassdoor.ni"},
        {"code": "CR", "name": "Costa Rica", "lang": "es", "currency": "CRC", "jobs_url": "indeed.co.cr,linkedin.com,computrabajo.com,costaricajobs.com,glassdoor.cr"},
        {"code": "PA", "name": "Panama", "lang": "es", "currency": "USD", "jobs_url": "indeed.com.pa,linkedin.com,computrabajo.com,panamajobs.com,glassdoor.pa"},
        {"code": "CO", "name": "Colombia", "lang": "es", "currency": "COP", "jobs_url": "indeed.co,linkedin.com,computrabajo.com,hipersuper.com,zoombam.com,glassdoor.co"},
        {"code": "VE", "name": "Venezuela", "lang": "es", "currency": "USD", "jobs_url": "indeed.co,linkedin.com,computrabajo.com,venezuelajob.com,glassdoor.ve"},
        {"code": "EC", "name": "Ecuador", "lang": "es", "currency": "USD", "jobs_url": "indeed.ec,linkedin.com,computrabajo.com,ecuadorjobs.com,glassdoor.ec"},
        {"code": "PE", "name": "Peru", "lang": "es", "currency": "PEN", "jobs_url": "indeed.pe,linkedin.com,computrabajo.com,bum.net,perujob.com,glassdoor.pe"},
        {"code": "BO", "name": "Bolivia", "lang": "es", "currency": "BOB", "jobs_url": "indeed.bo,linkedin.com,computrabajo.com,boliviajobs.com,glassdoor.bo"},
        {"code": "PY", "name": "Paraguay", "lang": "es", "currency": "PYG", "jobs_url": "indeed.com.py,linkedin.com,computrabajo.com,paraguayjobs.com,glassdoor.py"},
        {"code": "UY", "name": "Uruguay", "lang": "es", "currency": "UYU", "jobs_url": "indeed.com.uy,linkedin.com,computrabajo.com,uruguayjobs.com,glassdoor.uy"},
        {"code": "AR", "name": "Argentina", "lang": "es", "currency": "ARS", "jobs_url": "indeed.com.ar,linkedin.com,computrabajo.com,bum.net,jobui.com,glassdoor.ar"},
        {"code": "CL", "name": "Chile", "lang": "es", "currency": "CLP", "jobs_url": "indeed.cl,linkedin.com,computrabajo.com,laborum.com,chiletrabajos.cl,glassdoor.cl"},
        {"code": "BR", "name": "Brazil", "lang": "pt", "currency": "BRL", "jobs_url": "indeed.com.br,linkedin.com,Catho.com,vagas.com.br,ciadatotal.com,glassdoor.br"},
        {"code": "GY", "name": "Guyana", "lang": "en", "currency": "GYD", "jobs_url": "indeed.gy,linkedin.com,guyanajob.com,guyanaonline.com,glassdoor.gy"},
        {"code": "SR", "name": "Suriname", "lang": "nl", "currency": "SRD", "jobs_url": "indeed.sr,linkedin.com,careerssuriname.com,surinamejobs.com,glassdoor.sr"},
        {"code": "CU", "name": "Cuba", "lang": "es", "currency": "CUP", "jobs_url": "indeed.cu,linkedin.com,trabajo.org,cubajobs.com,glassdoor.cu"},
        {"code": "JM", "name": "Jamaica", "lang": "en", "currency": "JMD", "jobs_url": "indeed.com.jm,linkedin.com,jobsjamaica.com,jamaicajob.com,glassdoor.jm"},
        {"code": "HT", "name": "Haiti", "lang": "fr", "currency": "HTG", "jobs_url": "indeed.ht,linkedin.com,avsjobs.com,haitijob.com,glassdoor.ht"},
        {"code": "DO", "name": "Dominican Republic", "lang": "es", "currency": "DOP", "jobs_url": "indeed.com.do,linkedin.com,computrabajo.com,RDjobs.com,glassdoor.do"},
        {"code": "PR", "name": "Puerto Rico", "lang": "es", "currency": "USD", "jobs_url": "indeed.pr,linkedin.com,jobspr.com,boricajobs.com,glassdoor.pr"},
        {"code": "TT", "name": "Trinidad", "lang": "en", "currency": "TTD", "jobs_url": "indeed.tt,linkedin.com,caribbeanjobs.com,trinidadjobs.com,glassdoor.tt"},
        {"code": "BB", "name": "Barbados", "lang": "en", "currency": "BBD", "jobs_url": "indeed.bb,linkedin.com,caribbeanjobs.com,barbadosjobs.com,glassdoor.bb"},
        
        # ===== ASIA (50) =====
        {"code": "CN", "name": "China", "lang": "zh", "currency": "CNY", "jobs_url": "indeed.com.hk,linkedin.com,51job.com,zhaopin.com,liepin.com,lagou.com,zhilian.com,boss.com"},
        {"code": "HK", "name": "Hong Kong", "lang": "zh", "currency": "HKD", "jobs_url": "indeed.hk,linkedin.com,jobsDB.com,cpjobs.com,glassdoor.hk"},
        {"code": "TW", "name": "Taiwan", "lang": "zh", "currency": "TWD", "jobs_url": "indeed.com.tw,linkedin.com,104.com.tw,1111.com.tw,glassdoor.tw"},
        {"code": "MO", "name": "Macau", "lang": "zh", "currency": "MOP", "jobs_url": "indeed.mo,linkedin.com,macaujob.com,glassdoor.mo"},
        {"code": "JP", "name": "Japan", "lang": "ja", "currency": "JPY", "jobs_url": "indeed.co.jp,linkedin.com,rakuten.co.jp,type.jp,doda.jp,wantedly.com,glassdoor.jp"},
        {"code": "KR", "name": "South Korea", "lang": "ko", "currency": "KRW", "jobs_url": "indeed.co.kr,linkedin.com,saramin.co.kr,jobkorea.co.kr,wanted.co.kr,glassdoor.kr"},
        {"code": "KP", "name": "North Korea", "lang": "ko", "currency": "KPW", "jobs_url": "linkedin.com"},
        {"code": "IN", "name": "India", "lang": "hi", "currency": "INR", "jobs_url": "indeed.co.in,linkedin.com,naukri.com,monsterindia.com,shine.com,freshersworld.com,timesjobs.com,glassdoor.co.in"},
        {"code": "PK", "name": "Pakistan", "lang": "ur", "currency": "PKR", "jobs_url": "indeed.pk,linkedin.com,rozee.pk,glassdoor.pk,pakistanijob.com"},
        {"code": "BD", "name": "Bangladesh", "lang": "bn", "currency": "BDT", "jobs_url": "indeed.com.bd,linkedin.com,bdjobs.com,prothomalo.com,banglajob.com,glassdoor.bd"},
        {"code": "LK", "name": "Sri Lanka", "lang": "si", "currency": "LKR", "jobs_url": "indeed.lk,linkedin.com,ikman.lk,jobs.lk,glassdoor.lk"},
        {"code": "NP", "name": "Nepal", "lang": "ne", "currency": "NPR", "jobs_url": "indeed.com.np,linkedin.com,merojob.com,jobnepal.com,jobaxle.com,glassdoor.np"},
        {"code": "BT", "name": "Bhutan", "lang": "dz", "currency": "BTN", "jobs_url": "indeed.bt,linkedin.com,bnljobs.com,bhutanjobs.com,glassdoor.bt"},
        {"code": "MV", "name": "Maldives", "lang": "dv", "currency": "MVR", "jobs_url": "indeed.mv,linkedin.com,jobsmaldives.com,maldivianjobs.com,glassdoor.mv"},
        {"code": "AF", "name": "Afghanistan", "lang": "ps", "currency": "AFN", "jobs_url": "indeed.af,linkedin.com,AfghanistanJobs.com,afghanjobs.com,glassdoor.af"},
        {"code": "TJ", "name": "Tajikistan", "lang": "tg", "currency": "TJS", "jobs_url": "indeed.tj,linkedin.com,tajikjobs.com,tajikistanjobs.com,glassdoor.tj"},
        {"code": "TM", "name": "Turkmenistan", "lang": "tk", "currency": "TMT", "jobs_url": "indeed.tm,linkedin.com,turkmenjobs.com,glassdoor.tm"},
        {"code": "UZ", "name": "Uzbekistan", "lang": "uz", "currency": "UZS", "jobs_url": "indeed.uz,linkedin.com,job.uz,uzbekistanjobs.com,glassdoor.uz"},
        {"code": "KG", "name": "Kyrgyzstan", "lang": "ky", "currency": "KGS", "jobs_url": "indeed.kg,linkedin.com,el.kg,kyrgyzstanjobs.com,glassdoor.kg"},
        {"code": "KZ", "name": "Kazakhstan", "lang": "kk", "currency": "KZT", "jobs_url": "indeed.kz,linkedin.com,hh.kz,jobs.kz,enbek.kz,glassdoor.kz"},
        {"code": "MN", "name": "Mongolia", "lang": "mn", "currency": "MNT", "jobs_url": "indeed.mn,linkedin.com,job.mn,mongoliajobs.com,glassdoor.mn"},
        {"code": "MM", "name": "Myanmar", "lang": "my", "currency": "MMK", "jobs_url": "indeed.com.mm,linkedin.com,jobnet.com.mm,myanmarjobs.com,glassdoor.mm"},
        {"code": "TH", "name": "Thailand", "lang": "th", "currency": "THB", "jobs_url": "indeed.co.th,linkedin.com,jobThai.com,jobsDBthailand.com,glassdoor.co.th"},
        {"code": "LA", "name": "Laos", "lang": "lo", "currency": "LAK", "jobs_url": "indeed.la,linkedin.com,laojob.com,laosjobs.com,glassdoor.la"},
        {"code": "VN", "name": "Vietnam", "lang": "vi", "currency": "VND", "jobs_url": "indeed.vn,linkedin.com,vieclam.vn,vnworks.com,timviec.com.vn,glassdoor.vn"},
        {"code": "KH", "name": "Cambodia", "lang": "km", "currency": "KHR", "jobs_url": "indeed.kh,linkedin.com,cambojob.com,cambodiajobs.com,glassdoor.kh"},
        {"code": "MY", "name": "Malaysia", "lang": "ms", "currency": "MYR", "jobs_url": "indeed.my,linkedin.com,malaysiasearch.com,jobstreet.com.my,glassdoor.my"},
        {"code": "SG", "name": "Singapore", "lang": "en", "currency": "SGD", "jobs_url": "indeed.com.sg,linkedin.com,jobstreet.com.sg,mycareersfuture.gov.sg,glassdoor.sg"},
        {"code": "ID", "name": "Indonesia", "lang": "id", "currency": "IDR", "jobs_url": "indeed.co.id,linkedin.com,karir.com,lowongankerja.com,glints.com,glassdoor.co.id"},
        {"code": "BN", "name": "Brunei", "lang": "ms", "currency": "BND", "jobs_url": "indeed.bn,linkedin.com,jobbrunei.com,bruneijob.com,glassdoor.bn"},
        {"code": "PH", "name": "Philippines", "lang": "tl", "currency": "PHP", "jobs_url": "indeed.ph,linkedin.com,jobstreet.com.ph,Kalibrr.com,jobs.ph,glassdoor.ph"},
        {"code": "TL", "name": "East Timor", "lang": "tet", "currency": "USD", "jobs_url": "indeed.tl,linkedin.com,timorjobs.com,glassdoor.tl"},
        {"code": "IR", "name": "Iran", "lang": "fa", "currency": "IRR", "jobs_url": "indeed.ir,linkedin.com,jobIran.com,iranjobs.com,glassdoor.ir"},
        {"code": "IQ", "name": "Iraq", "lang": "ar", "currency": "IQD", "jobs_url": "indeed.iq,linkedin.com,iraqijob.com,iraqjobs.com,glassdoor.iq"},
        {"code": "TR", "name": "Turkey", "lang": "tr", "currency": "TRY", "jobs_url": "indeed.com.tr,linkedin.com,kariyer.net,insaniz.com,glassdoor.com.tr"},
        {"code": "AZ", "name": "Azerbaijan", "lang": "az", "currency": "AZN", "jobs_url": "indeed.az,linkedin.com,jobsearch.az,azerbaijanjobs.com,glassdoor.az"},
        {"code": "GE", "name": "Georgia", "lang": "ka", "currency": "GEL", "jobs_url": "indeed.ge,linkedin.com,hr.ge,georgiajobs.com,glassdoor.ge"},
        {"code": "AM", "name": "Armenia", "lang": "hy", "currency": "AMD", "jobs_url": "indeed.am,linkedin.com,ararattv.am,armeniajobs.com,glassdoor.am"},
        {"code": "YE", "name": "Yemen", "lang": "ar", "currency": "YER", "jobs_url": "indeed.ye,linkedin.com,yemen-jobs.com,glassdoor.ye"},
        {"code": "SA", "name": "Saudi Arabia", "lang": "ar", "currency": "SAR", "jobs_url": "indeed.com.sa,linkedin.com,jobsaudi.com,GulfTalent.com,glassdoor.sa"},
        {"code": "AE", "name": "UAE", "lang": "ar", "currency": "AED", "jobs_url": "indeed.ae,linkedin.com,GulfTalent.com,jobrapido.ae,dubizzle.com,glassdoor.ae"},
        {"code": "QA", "name": "Qatar", "lang": "ar", "currency": "QAR", "jobs_url": "indeed.qa,linkedin.com,GulfTalent.com,jobQatar.com,glassdoor.qa"},
        {"code": "KW", "name": "Kuwait", "lang": "ar", "currency": "KWD", "jobs_url": "indeed.com.kw,linkedin.com,GulfTalent.com,jobskwt.com,glassdoor.kw"},
        {"code": "BH", "name": "Bahrain", "lang": "ar", "currency": "BHD", "jobs_url": "indeed.com.bh,linkedin.com,GulfTalent.com,bahrainijob.com,glassdoor.bh"},
        {"code": "OM", "name": "Oman", "lang": "ar", "currency": "OMR", "jobs_url": "indeed.com.om,linkedin.com,GulfTalent.com,OmanJob.com,glassdoor.om"},
        {"code": "IL", "name": "Israel", "lang": "he", "currency": "ILS", "jobs_url": "indeed.co.il,linkedin.com,jobmaster.co.il,glassdoor.co.il"},
        {"code": "PS", "name": "Palestine", "lang": "ar", "currency": "ILS", "jobs_url": "indeed.ps,linkedin.com,PalJobs.com,palestinejobs.com,glassdoor.ps"},
        {"code": "JO", "name": "Jordan", "lang": "ar", "currency": "JOD", "jobs_url": "indeed.jo,linkedin.com,jobam.net,jordanjobs.com,glassdoor.jo"},
        {"code": "LB", "name": "Lebanon", "lang": "ar", "currency": "LBP", "jobs_url": "indeed.com.lb,linkedin.com,daleel-madani.org,hirelebanese.com,glassdoor.lb"},
        {"code": "SY", "name": "Syria", "lang": "ar", "currency": "SYP", "jobs_url": "indeed.sy,linkedin.com,syriajob.com,glassdoor.sy"},
        
        # ===== RUSSIA & CIS (15) =====
        {"code": "RU", "name": "Russia", "lang": "ru", "currency": "RUB", "jobs_url": "indeed.ru,linkedin.com,hh.ru,superjob.ru,zarplata.ru,rabota.ru"},
        {"code": "BY", "name": "Belarus", "lang": "be", "currency": "BYR", "jobs_url": "indeed.by,linkedin.com,rabota.by,tut.by"},
        {"code": "UA", "name": "Ukraine", "lang": "uk", "currency": "UAH", "jobs_url": "indeed.ua,linkedin.com,work.ua,hh.ua,robota.ua"},
        {"code": "KZ", "name": "Kazakhstan", "lang": "kk", "currency": "KZT", "jobs_url": "indeed.kz,linkedin.com,hh.kz,jobik.kz"},
        {"code": "UZ", "name": "Uzbekistan", "lang": "uz", "currency": "UZS", "jobs_url": "indeed.uz,linkedin.com,job.uz"},
        {"code": "TJ", "name": "Tajikistan", "lang": "tg", "currency": "TJS", "jobs_url": "indeed.tj,linkedin.com"},
        {"code": "KG", "name": "Kyrgyzstan", "lang": "ky", "currency": "KGS", "jobs_url": "indeed.kg,linkedin.com"},
        {"code": "TM", "name": "Turkmenistan", "lang": "tk", "currency": "TMT", "jobs_url": "indeed.tm,linkedin.com"},
        {"code": "AZ", "name": "Azerbaijan", "lang": "az", "currency": "AZN", "jobs_url": "indeed.az,linkedin.com,jobsearch.az"},
        {"code": "GE", "name": "Georgia", "lang": "ka", "currency": "GEL", "jobs_url": "indeed.ge,linkedin.com"},
        {"code": "AM", "name": "Armenia", "lang": "hy", "currency": "AMD", "jobs_url": "indeed.am,linkedin.com"},
        {"code": "MD", "name": "Moldova", "lang": "ro", "currency": "MDL", "jobs_url": "indeed.md,linkedin.com"},
        
        # ===== AFRICA (55) =====
        {"code": "ZA", "name": "South Africa", "lang": "en", "currency": "ZAR", "jobs_url": "indeed.co.za,linkedin.com,careers24.com,pnet.co.za,jobmail.co.za,glassdoor.co.za"},
        {"code": "NG", "name": "Nigeria", "lang": "en", "currency": "NGN", "jobs_url": "indeed.ng,linkedin.com,jobberman.com,careers24.com.ng,glassdoor.ng"},
        {"code": "EG", "name": "Egypt", "lang": "ar", "currency": "EGP", "jobs_url": "indeed.com.eg,linkedin.com,wuzzuf.net,forasna.com,glassdoor.com.eg"},
        {"code": "MA", "name": "Morocco", "lang": "ar", "currency": "MAD", "jobs_url": "indeed.ma,linkedin.com,rekrute.com,emploimaroc.com,glassdoor.ma"},
        {"code": "DZ", "name": "Algeria", "lang": "ar", "currency": "DZD", "jobs_url": "indeed.dz,linkedin.com,dzLinkedin.com,algeriajobs.com,glassdoor.dz"},
        {"code": "TN", "name": "Tunisia", "lang": "ar", "currency": "TND", "jobs_url": "indeed.tn,linkedin.com,tunisianet.com.tn,glassdoor.tn"},
        {"code": "LY", "name": "Libya", "lang": "ar", "currency": "LYD", "jobs_url": "indeed.ly,linkedin.com,libyanjobs.com,glassdoor.ly"},
        {"code": "SD", "name": "Sudan", "lang": "ar", "currency": "SDG", "jobs_url": "indeed.sd,linkedin.com,sudanjobs.com,glassdoor.sd"},
        {"code": "ET", "name": "Ethiopia", "lang": "am", "currency": "ETB", "jobs_url": "indeed.et,linkedin.com,ethiojobs.net,ethiopiajobs.com,glassdoor.et"},
        {"code": "KE", "name": "Kenya", "lang": "sw", "currency": "KES", "jobs_url": "indeed.co.ke,linkedin.com,brightermonday.co.ke,finda.co.ke,glassdoor.co.ke"},
        {"code": "TZ", "name": "Tanzania", "lang": "sw", "currency": "TZS", "jobs_url": "indeed.co.tz,linkedin.com,ajira.go.tz,tanzaniajobs.com,glassdoor.tz"},
        {"code": "UG", "name": "Uganda", "lang": "en", "currency": "UGX", "jobs_url": "indeed.co.ug,linkedin.com,ugandajob.com,ugandajobs.com,glassdoor.ug"},
        {"code": "GH", "name": "Ghana", "lang": "en", "currency": "GHS", "jobs_url": "indeed.com.gh,linkedin.com,jobGhana.com,ghanajobs.com,glassdoor.gh"},
        {"code": "CI", "name": "Ivory Coast", "lang": "fr", "currency": "XOF", "jobs_url": "indeed.ci,linkedin.com,emploicc.com,ivorycoastjobs.com,glassdoor.ci"},
        {"code": "SN", "name": "Senegal", "lang": "fr", "currency": "XOF", "jobs_url": "indeed.sn,linkedin.com,emploisenegal.com,senegaljobs.com,glassdoor.sn"},
        {"code": "CM", "name": "Cameroon", "lang": "fr", "currency": "XAF", "jobs_url": "indeed.cm,linkedin.com,cameroonjobs.com,glassdoor.cm"},
        {"code": "AO", "name": "Angola", "lang": "pt", "currency": "AOA", "jobs_url": "indeed.ao,linkedin.com,emprego.co.ao,angolajobs.com,glassdoor.ao"},
        {"code": "MZ", "name": "Mozambique", "lang": "pt", "currency": "MZN", "jobs_url": "indeed.mz,linkedin.com,emprego.co.mz,mozambiquejobs.com,glassdoor.mz"},
        {"code": "ZM", "name": "Zambia", "lang": "en", "currency": "ZMW", "jobs_url": "indeed.co.zm,linkedin.com,zambia.jobs,zambiajobs.com,glassdoor.zm"},
        {"code": "ZW", "name": "Zimbabwe", "lang": "en", "currency": "ZWL", "jobs_url": "indeed.co.zw,linkedin.com,zimbabwejobs.com,glassdoor.zw"},
        {"code": "BW", "name": "Botswana", "lang": "en", "currency": "BWP", "jobs_url": "indeed.co.bw,linkedin.com,botswanajob.com,glassdoor.bw"},
        {"code": "NA", "name": "Namibia", "lang": "en", "currency": "NAD", "jobs_url": "indeed.na,linkedin.com,namibianjobs.com,glassdoor.na"},
        {"code": "LS", "name": "Lesotho", "lang": "en", "currency": "LSL", "jobs_url": "indeed.ls,linkedin.com,lesothojobs.com,glassdoor.ls"},
        {"code": "SZ", "name": "Eswatini", "lang": "en", "currency": "SZL", "jobs_url": "indeed.sz,linkedin.com,swazijobs.com,glassdoor.sz"},
        {"code": "MW", "name": "Malawi", "lang": "en", "currency": "MWK", "jobs_url": "indeed.mw,linkedin.com,malawijobs.com,glassdoor.mw"},
        {"code": "MU", "name": "Mauritius", "lang": "en", "currency": "MUR", "jobs_url": "indeed.mu,linkedin.com,mauritiusjobs.com,glassdoor.mu"},
        {"code": "SC", "name": "Seychelles", "lang": "fr", "currency": "SCR", "jobs_url": "indeed.sc,linkedin.com,seychellesjobs.com,glassdoor.sc"},
        {"code": "MR", "name": "Mausamnia", "lang": "ar", "currency": "MRU", "jobs_url": "indeed.mr,linkedin.com,maurtaniajobs.com,glassdoor.mr"},
        {"code": "ML", "name": "Mali", "lang": "fr", "currency": "XOF", "jobs_url": "indeed.ml,linkedin.com,malijobs.com,glassdoor.ml"},
        {"code": "NE", "name": "Niger", "lang": "fr", "currency": "XOF", "jobs_url": "indeed.ne,linkedin.com,nigerjobs.com,glassdoor.ne"},
        {"code": "BF", "name": "Burkina Faso", "lang": "fr", "currency": "XOF", "jobs_url": "indeed.bf,linkedin.com,burkinajobs.com,glassdoor.bf"},
        {"code": "TD", "name": "Chad", "lang": "fr", "currency": "XAF", "jobs_url": "indeed.td,linkedin.com,chadjobs.com,glassdoor.td"},
        {"code": "CF", "name": "Central African Rep.", "lang": "fr", "currency": "XAF", "jobs_url": "indeed.cf,linkedin.com,carjobs.com,glassdoor.cf"},
        {"code": "CG", "name": "Congo", "lang": "fr", "currency": "XAF", "jobs_url": "indeed.cg,linkedin.com,congojobs.com,glassdoor.cg"},
        {"code": "CD", "name": "DR Congo", "lang": "fr", "currency": "CDF", "jobs_url": "indeed.cd,linkedin.com,rdcjobs.com,glassdoor.cd"},
        {"code": "GA", "name": "Gabon", "lang": "fr", "currency": "XAF", "jobs_url": "indeed.ga,linkedin.com,gabojobs.com,glassdoor.ga"},
        {"code": "GQ", "name": "Equatorial Guinea", "lang": "es", "currency": "XAF", "jobs_url": "indeed.gq,linkedin.com,eqjobs.com,glassdoor.gq"},
        {"code": "DJ", "name": "Djibouti", "lang": "fr", "currency": "DJF", "jobs_url": "indeed.dj,linkedin.com,djiboutijobs.com,glassdoor.dj"},
        {"code": "SO", "name": "Somalia", "lang": "so", "currency": "SOS", "jobs_url": "indeed.so,linkedin.com,somalijobs.com,glassdoor.so"},
        {"code": "ER", "name": "Eritrea", "lang": "ti", "currency": "ERN", "jobs_url": "indeed.er,linkedin.com,eritreajobs.com,glassdoor.er"},
        {"code": "SS", "name": "South Sudan", "lang": "en", "currency": "SSP", "jobs_url": "indeed.ss,linkedin.com,ssjobs.com,glassdoor.ss"},
        {"code": "BI", "name": "Burundi", "lang": "fr", "currency": "BIF", "jobs_url": "indeed.bi,linkedin.com,burundijobs.com,glassdoor.bi"},
        {"code": "RW", "name": "Rwanda", "lang": "rw", "currency": "RWF", "jobs_url": "indeed.rw,linkedin.com,rwandajob.com,glassdoor.rw"},
        {"code": "MG", "name": "Madagascar", "lang": "mg", "currency": "MGA", "jobs_url": "indeed.mg,linkedin.com,madagascarjobs.com,glassdoor.mg"},
        {"code": "KM", "name": "Comoros", "lang": "ar", "currency": "KMF", "jobs_url": "indeed.km,linkedin.com,comorosjobs.com,glassdoor.km"},
        {"code": "ST", "name": "Sao Tome", "lang": "pt", "currency": "STN", "jobs_url": "indeed.st,linkedin.com,saotomejobs.com,glassdoor.st"},
        {"code": "CV", "name": "Cape Verde", "lang": "pt", "currency": "CVE", "jobs_url": "indeed.cv,linkedin.com,capeverdejobs.com,glassdoor.cv"},
        {"code": "GW", "name": "Guinea-Bissau", "lang": "pt", "currency": "XOF", "jobs_url": "indeed.gw,linkedin.com,guineabissaujobs.com,glassdoor.gw"},
        {"code": "GM", "name": "Gambia", "lang": "en", "currency": "GMD", "jobs_url": "indeed.gm,linkedin.com,gambiajobs.com,glassdoor.gm"},
        {"code": "SL", "name": "Sierra Leone", "lang": "en", "currency": "SLL", "jobs_url": "indeed.sl,linkedin.com,sierraleonejobs.com,glassdoor.sl"},
        {"code": "LR", "name": "Liberia", "lang": "en", "currency": "LRD", "jobs_url": "indeed.lr,linkedin.com,liberiajobs.com,glassdoor.lr"},
        {"code": "GN", "name": "Guinea", "lang": "fr", "currency": "GNF", "jobs_url": "indeed.gn,linkedin.com,guineajobs.com,glassdoor.gn"},
        
        # ===== OCEANIA (15) =====
        {"code": "AU", "name": "Australia", "lang": "en", "currency": "AUD", "jobs_url": "indeed.com.au,linkedin.com,seek.com.au,jobsearch.com.au,careerone.com.au,glassdoor.com.au"},
        {"code": "NZ", "name": "New Zealand", "lang": "en", "currency": "NZD", "jobs_url": "indeed.co.nz,linkedin.com,seek.co.nz,trademe.co.nz,jobs.govt.nz,glassdoor.co.nz"},
        {"code": "FJ", "name": "Fiji", "lang": "en", "currency": "FJD", "jobs_url": "indeed.fj,linkedin.com,fijijob.com,fijijobs.com,glassdoor.fj"},
        {"code": "PG", "name": "Papua New Guinea", "lang": "en", "currency": "PGK", "jobs_url": "indeed.pg,linkedin.com,pngjobs.com,glassdoor.pg"},
        {"code": "SB", "name": "Solomon Islands", "lang": "en", "currency": "SBD", "jobs_url": "indeed.sb,linkedin.com,solomonjobs.com,glassdoor.sb"},
        {"code": "VU", "name": "Vanuatu", "lang": "bi", "currency": "VUV", "jobs_url": "indeed.vu,linkedin.com,vanuatujobs.com,glassdoor.vu"},
        {"code": "WS", "name": "Samoa", "lang": "sm", "currency": "WST", "jobs_url": "indeed.ws,linkedin.com,samoajobs.com,glassdoor.ws"},
        {"code": "TO", "name": "Tonga", "lang": "to", "currency": "TOP", "jobs_url": "indeed.to,linkedin.com,tongajobs.com,glassdoor.to"},
        {"code": "PW", "name": "Palau", "lang": "en", "currency": "USD", "jobs_url": "indeed.pw,linkedin.com,palaujobs.com,glassdoor.pw"},
        {"code": "KI", "name": "Kiribati", "lang": "en", "currency": "AUD", "jobs_url": "indeed.ki,linkedin.com,kiribatajobs.com,glassdoor.ki"},
        {"code": "FM", "name": "Micronesia", "lang": "en", "currency": "USD", "jobs_url": "indeed.fm,linkedin.com,micronesiajobs.com,glassdoor.fm"},
        {"code": "MH", "name": "Marshall Islands", "lang": "en", "currency": "USD", "jobs_url": "indeed.mh,linkedin.com,marshallislandjobs.com,glassdoor.mh"},
        {"code": "NR", "name": "Nauru", "lang": "en", "currency": "AUD", "jobs_url": "indeed.nr,linkedin.com,naurujobs.com,glassdoor.nr"},
        {"code": "TV", "name": "Tuvalu", "lang": "en", "currency": "TVD", "jobs_url": "indeed.tv,linkedin.com,tuvalujobs.com,glassdoor.tv"},
        {"code": "CK", "name": "Cook Islands", "lang": "en", "currency": "NZD", "jobs_url": "indeed.ck,linkedin.com,cookislandsjobs.com,glassdoor.ck"},
    ])
    
    # JOB PLATFORMS (50+)
    JOB_PLATFORMS: List[Dict] = field(default_factory=lambda: [
        # ===== GLOBAL GIANTS =====
        {"name": "LinkedIn", "url": "linkedin.com", "auto_apply": True, "global": True},
        {"name": "Indeed", "url": "indeed.com", "auto_apply": True, "global": True},
        {"name": "Glassdoor", "url": "glassdoor.com", "auto_apply": True, "global": True},
        {"name": "Monster", "url": "monster.com", "auto_apply": True, "global": True},
        {"name": "CareerBuilder", "url": "careerbuilder.com", "auto_apply": True, "global": True},
        {"name": "ZipRecruiter", "url": "ziprecruiter.com", "auto_apply": True, "global": True},
        {"name": "SimplyHired", "url": "simplyhired.com", "auto_apply": True, "global": True},
        {"name": "Snagajob", "url": "snagajob.com", "auto_apply": True, "global": True},
        {"name": "Talent", "url": "talent.com", "auto_apply": True, "global": True},
        
        # ===== EUROPE =====
        {"name": "InfoJobs", "url": "infojobs.net", "auto_apply": True, "countries": "ES,IT,BR,MX"},
        {"name": "StepStone", "url": "stepstone.de", "auto_apply": True, "countries": "DE,AT,BE,NL,FR"},
        {"name": "Jobs.cz", "url": "jobs.cz", "auto_apply": True, "countries": "CZ"},
        {"name": "Pracuj.pl", "url": "pracuj.pl", "auto_apply": True, "countries": "PL"},
        {"name": "Intermediair", "url": "intermediair.nl", "auto_apply": True, "countries": "NL"},
        {"name": "Jobindex", "url": "jobindex.dk", "auto_apply": True, "countries": "DK"},
        {"name": "Arbetsformedlingen", "url": "arbetsformedlingen.se", "auto_apply": True, "countries": "SE"},
        {"name": "Finn", "url": "finn.no", "auto_apply": True, "countries": "NO"},
        {"name": "IrishJobs", "url": "irishjobs.ie", "auto_apply": True, "countries": "IE"},
        {"name": "CV-Library", "url": "cv-library.co.uk", "auto_apply": True, "countries": "GB"},
        {"name": "Reed", "url": "reed.co.uk", "auto_apply": True, "countries": "GB"},
        {"name": "Pole-Emploi", "url": "pole-emploi.fr", "auto_apply": True, "countries": "FR"},
        {"name": "Apec", "url": "apec.fr", "auto_apply": True, "countries": "FR"},
        {"name": "Trabajo", "url": "trabajo.org", "auto_apply": True, "countries": "ES"},
        {"name": "Work.ua", "url": "work.ua", "auto_apply": True, "countries": "UA"},
        {"name": "HH.ru", "url": "hh.ru", "auto_apply": True, "countries": "RU"},
        {"name": "Superjob", "url": "superjob.ru", "auto_apply": True, "countries": "RU"},
        
        # ===== MIDDLE EAST / GULF =====
        {"name": "Bayt", "url": "bayt.com", "auto_apply": True, "countries": "AE,SA,QA,KW,BH,OM,LB,EG"},
        {"name": "GulfTalent", "url": "gulftalent.com", "auto_apply": True, "countries": "AE,SA,QA,KW,BH,OM"},
        {"name": "Dubizzle", "url": "dubizzle.com", "auto_apply": True, "countries": "AE,SA,EG"},
        {"name": "Wazajobs", "url": "wazajobs.com", "auto_apply": True, "countries": "SA,AE"},
        {"name": "NaukriGulf", "url": "naukrigulf.com", "auto_apply": True, "countries": "AE,SA,QA,KW"},
        {"name": "MonsterGulf", "url": "monstergulf.com", "auto_apply": True, "countries": "AE,SA,QA,KW"},
        {"name": "GulfTalent", "url": "gulftalent.com", "auto_apply": True, "countries": "AE,SA,QA,KW,BH,OM"},
        
        # ===== ASIA =====
        {"name": "Naukri", "url": "naukri.com", "auto_apply": True, "countries": "IN"},
        {"name": "MonsterIndia", "url": "monsterindia.com", "auto_apply": True, "countries": "IN"},
        {"name": "Shine", "url": "shine.com", "auto_apply": True, "countries": "IN"},
        {"name": "TimesJobs", "url": "timesjobs.com", "auto_apply": True, "countries": "IN"},
        {"name": "51job", "url": "51job.com", "auto_apply": True, "countries": "CN"},
        {"name": "Zhaopin", "url": "zhaopin.com", "auto_apply": True, "countries": "CN"},
        {"name": "Liepin", "url": "liepin.com", "auto_apply": True, "countries": "CN"},
        {"name": "Lagou", "url": "lagou.com", "auto_apply": True, "countries": "CN"},
        {"name": "Boss Zhipin", "url": "zhipin.com", "auto_apply": True, "countries": "CN"},
        {"name": "Saramin", "url": "saramin.co.kr", "auto_apply": True, "countries": "KR"},
        {"name": "JobKorea", "url": "jobkorea.co.kr", "auto_apply": True, "countries": "KR"},
        {"name": "Wanted", "url": "wanted.co.kr", "auto_apply": True, "countries": "KR"},
        {"name": "Rakuten", "url": "rakuten.co.jp", "auto_apply": True, "countries": "JP"},
        {"name": "Doda", "url": "doda.jp", "auto_apply": True, "countries": "JP"},
        {"name": "JobStreet", "url": "jobstreet.com", "auto_apply": True, "countries": "MY,SG,PH,ID"},
        {"name": "JobsDB", "url": "jobsdb.com", "auto_apply": True, "countries": "HK,TH,AU,NZ"},
        {"name": "MyCareersFuture", "url": "mycareersfuture.gov.sg", "auto_apply": True, "countries": "SG"},
        
        # ===== AFRICA =====
        {"name": "Careers24", "url": "careers24.com", "auto_apply": True, "countries": "ZA"},
        {"name": "Pnet", "url": "pnet.co.za", "auto_apply": True, "countries": "ZA"},
        {"name": "Jobmail", "url": "jobmail.co.za", "auto_apply": True, "countries": "ZA"},
        {"name": "Jobberman", "url": "jobberman.com", "auto_apply": True, "countries": "NG,GH,KE"},
        {"name": "BrighterMonday", "url": "brightermonday.co.ke", "auto_apply": True, "countries": "KE,TZ,UG"},
        {"name": "Wuzzuf", "url": "wuzzuf.net", "auto_apply": True, "countries": "EG"},
        {"name": "Rekrute", "url": "rekrute.com", "auto_apply": True, "countries": "MA"},
        {"name": "Ethiojobs", "url": "ethiojobs.net", "auto_apply": True, "countries": "ET"},
        
        # ===== LATIN AMERICA =====
        {"name": "Bumeran", "url": "bumeran.com", "auto_apply": True, "countries": "AR,CL,PE,MX"},
        {"name": "Computrabajo", "url": "computrabajo.com", "auto_apply": True, "countries": "MX,CO,AR,CL,PE,EC"},
        {"name": "Catho", "url": "catho.com.br", "auto_apply": True, "countries": "BR"},
        {"name": "Vagas", "url": "vagas.com.br", "auto_apply": True, "countries": "BR"},
        {"name": "Laborum", "url": "laborum.com", "auto_apply": True, "countries": "CL,PE,EC"},
        
        # ===== OCEANIA =====
        {"name": "Seek", "url": "seek.com.au", "auto_apply": True, "countries": "AU,NZ"},
        {"name": "CareerOne", "url": "careerone.com.au", "auto_apply": True, "countries": "AU"},
        
        # ===== LEBANON =====
        {"name": "Daleel Madani", "url": "daleel-madani.org", "auto_apply": True, "countries": "LB"},
        {"name": "HireLebanese", "url": "hirelebanese.com", "auto_apply": True, "countries": "LB"},
    ])
    
    # EMAIL PATTERNS (100+)
    EMAIL_PATTERNS: List[str] = field(default_factory=lambda: [
        # English - Primary
        "careers@{domain}", "jobs@{domain}", "hr@{domain}", "recruitment@{domain}",
        "hiring@{domain}", "talent@{domain}", "employment@{domain}", "info@{domain}",
        "contact@{domain}", "admin@{domain}", "apply@{domain}", "job@{domain}",
        "vacancies@{domain}", "openings@{domain}", "resumes@{domain}", "resume@{domain}",
        "recruit@{domain}", "personnel@{domain}", "staffing@{domain}", "work@{domain}",
        "hello@{domain}", "team@{domain}", "office@{domain}", "business@{domain}",
        "corporate@{domain}", "operations@{domain}", "support@{domain}", "accounts@{domain}",
        "enquiries@{domain}", "general@{domain}", "mail@{domain}", "post@{domain}",
        "ask@{domain}", "query@{domain}", "getintouch@{domain}", "reach@{domain}",
        "connect@{domain}", "join@{domain}", "partner@{domain}", "sales@{domain}",
        "marketing@{domain}", "hrrecruitment@{domain}", "humanresources@{domain}",
        "peopleteam@{domain}", "talentacquisition@{domain}", "employerbranding@{domain}",
        "careers-hr@{domain}", "jobapply@{domain}", "jobs-hr@{domain}",
        "vacancy@{domain}", "applications@{domain}", "applicants@{domain}",
        "hiring-team@{domain}", "recruiting@{domain}", "staff@{domain}",
        "workforus@{domain}", "joinus@{domain}", "career@{domain}",
        # German
        "karriere@{domain}", "personal@{domain}", "bewerbung@{domain}",
        "jobs@{domain}", "arbeitsstellen@{domain}",
        # French
        "carrieres@{domain}", "rh@{domain}", "recrutement@{domain}",
        "emploi@{domain}", "ressources-humaines@{domain}", "postuler@{domain}",
        # Spanish
        "empleo@{domain}", "recursos-humanos@{domain}", "contratacion@{domain}",
        "rrhh@{domain}", "bolsadetrabajo@{domain}",
        # Portuguese
        "carreiras@{domain}", "recursos-humanos@{domain}", "recrutamento@{domain}",
        "vagas@{domain}", "emprego@{domain}",
        # Chinese
        "career@{domain}", "jobs@{domain}", "recruit@{domain}",
        "hr@{domain}", "careers@{domain}",
        # Russian
        "kadry@{domain}", "personal@{domain}", "trud@{domain}",
        "rabota@{domain}", "resume@{domain}",
        # Arabic
        "hr@{domain}", "jobs@{domain}", "careers@{domain}",
        "recruitment@{domain}", "hiring@{domain}",
        # Dutch
        "vacatures@{domain}", "personeel@{domain}",
        # Italian
        "carriere@{domain}", "risorseumane@{domain}", "reclutamento@{domain}",
        "lavoro@{domain}", "offertedilavoro@{domain}",
        # Japanese
        "saiyo@{domain}", "recruit@{domain}", "career@{domain}",
        "career@{domain}", "jobs@{domain}", "recruit@{domain}",
        # Korean
        "career@{domain}", "recruit@{domain}", "jobs@{domain}",
        # Extra patterns
        "inbox@{domain}", "mails@{domain}", "hr-department@{domain}",
        "human-resources@{domain}", "people@{domain}", "culture@{domain}",
        "talent@{domain}", "peopleops@{domain}", "people-team@{domain}",
        "hiring-manager@{domain}", "recruiter@{domain}", "talent-acquisition@{domain}",
    ])

# Create global config instance
ULTIMATE_CONFIG = UltimateConfig()


# ============================================================================
# ULTIMATE CONFIG INSTANCE
# ============================================================================
CONFIG = UltimateConfig()

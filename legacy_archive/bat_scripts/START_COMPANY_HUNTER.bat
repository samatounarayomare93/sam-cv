@echo off
title RITA COMPANY HUNTER - MAXIMUM TARGETING
color 0C
cls

echo.
echo  ███████╗ ██████╗ ███╗   ██╗ █████╗ ██╗     ███████╗              
echo  ██╔════╝██╔═══██╗████╗  ██║██╔══██╗██║     ██╔════╝              
echo  █████╗  ██║   ██║██╔██╗ ██║███████║██║     █████╗                
echo  ██╔══╝  ██║   ██║██║╚██╗██║██╔══██║██║     ██╔══╝                
echo  ██║     ╚██████╔╝██║ ╚████║██║  ██║███████╗███████╗              
echo  ╚═╝      ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚══════╝              
echo.
echo  ██████╗ ███████╗███████╗ ██████╗██╗   ██╗███████╗                
echo  ██╔══██╗██╔════╝██╔════╝██╔════╝██║   ██║██╔════╝                
echo  ██████╔╝█████╗  ███████╗██║     ██║   ██║█████╗                  
echo  ██╔══██╗██╔══╝  ╚════██║██║     ██║   ██║██╔══╝                  
echo  ██║  ██║███████╗███████║╚██████╗╚██████╔╝███████╗                
echo  ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚══════╝                
echo.
echo  ███╗   ███╗██╗██████╗ ███╗   ██╗██╗ ██████╗ ██╗  ██╗████████╗ 
echo  ████╗ ████║██║██╔══██╗████╗  ██║██║██╔════╝ ██║  ██║╚══██╔══╝ 
echo  ██╔████╔██║██║██████╔╝██╔██╗ ██║██║██║  ███╗███████║   ██║    
echo  ██║╚██╔╝██║██║██╔═══╝ ██║╚██╗██║██║██║   ██║██╔══██║   ██║    
echo  ██║ ╚═╝ ██║██║██║     ██║ ╚████║██║╚██████╔╝██║  ██║   ██║    
echo  ╚═╝     ╚═╝╚═╝╚═╝     ╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝    
echo.
echo  ═══════════════════════════════════════════════════════════════════════
echo                    MAXIMUM COMPANY TARGETING ENGINE
echo  ═══════════════════════════════════════════════════════════════════════
echo.
echo  [TARGET SOURCES]
echo  ---------------------------------------------------------------------------
echo  [1] YellowPages USA    - Millions of US companies                      
echo  [2] YellowPages Intl   - UAE, KSA, Australia, UK, Canada             
echo  [3] LinkedIn           - Company directory                             
echo  [4] Google            - Business listings                              
echo  [5] Crunchbase        - Tech companies                                
echo  [6] Job Boards        - Indeed, Glassdoor, Monster companies         
echo  [7] ALL SOURCES       - Maximum coverage (RECOMMENDED)               
echo  ---------------------------------------------------------------------------
echo.
echo  [OPTIONS]
echo  [A] Hunt Only        - Discover companies and queue emails            
echo  [B] Hunt + Send       - Full automation (discover and send)             
echo  [C] Send Only         - Send queued emails                            
echo  [D] Statistics        - View database stats                           
echo.
echo  ═══════════════════════════════════════════════════════════════════════
echo.

python company_hunter.py

echo.
echo [COMPLETE] Company Hunter finished!
pause
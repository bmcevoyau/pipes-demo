BEGIN {
  nf = split("Jarrah,Kiara,Aden,Tanisha,Coen,Marlee,Djalu,Shanaya,Bailey,Ngaire,Tyrone,Leah,Corey,Amara,Dwayne,Talia,Kelton,Bindi,Rhys,Yindi,Marcus,Ellery,Kalarni,Brodie,Nerida,Jesse,Charmaine,Liam,Kirra,Owen,Shania,Declan,Mia,Blake,Alinta,Cody,Jedda,Noah,Warra,Ruby,Hayden,Lowanna,Jack,Tarni,Ethan,Kayleen,Sam,Dana,Jarrah,Nyah,Beau,Tjandamurra,Grace,Kobi,Lila,Reuben,Maali,Sienna,Wesley, Living",fn,",")
  nl = split("Nguyen,Bropho,Councillor,Ryan,Bennell,Hayes,Jetta,Little,Ugle,Walley,Yarran,Kelly,Michael,Dann,Garlett,Wynne,Champion,Farrell,Pickett,Riley,Stack,Roberts,Collard,Krakouer,Narkle,Blurton,Cameron,Comeagain,Egan,Hansen,Isaacs,Jones,Kickett,Miller,Ninyette,Oxenham,Penny,Quartermaine,Reibel,Smith,Taylor,Valli,Winmar,Yappo,Abdullah,Baxter,Coyne,Hill,Woods,Gray,Doolan,Pryor,Cox,Ryder,Warrell,Mippy,Boddington,Indich,Jacobs,Mourish",ln,",")

  # role|service_line|employment_type|roster|site_mode|day_rate|count|skills(comma)
  n=0
  roles[++n]="Trades Assistant|Industrial|Labour Hire|2:1 FIFO|pilbara|560|46|WHT,CSE,HR,C11,WCARD,FA"
  roles[++n]="Boilermaker|Industrial|Labour Hire|2:1 FIFO|pilbara|960|26|HR,CSE,WHT,C11,WCARD"
  roles[++n]="HD Diesel Fitter|Industrial|Labour Hire|8:6 FIFO|pilbara|1080|24|HR,C11,WCARD,FA,4WD"
  roles[++n]="Plant Operator|Industrial|Casual|8:6 FIFO|pilbara|780|22|HR,C11,WCARD,4WD,FA"
  roles[++n]="Scaffolder|Industrial|Casual|2:1 FIFO|pilbara|900|18|WHT,C11,WCARD,FA"
  roles[++n]="Rigger / Dogger|Industrial|Casual|2:1 FIFO|pilbara|1020|14|DOGRIG,WHT,CSE,C11,WCARD"
  roles[++n]="Auto Electrician|Industrial|Permanent|2:1 FIFO|pilbara|1040|10|C11,WCARD,FA,WHT"
  roles[++n]="Blast/Vac Operator|Industrial|Casual|2:1 FIFO|pilbara|720|8|CSE,WHT,WCARD,C11"
  roles[++n]="Industrial Supervisor|Industrial|Permanent|2:1 FIFO|pilbara|1240|8|HR,C11,WCARD,FA,CSE"
  roles[++n]="Environmental Technician|Environmental|Permanent|9 day fortnight|pilbara|680|28|4WD,WCARD,FA,TM"
  roles[++n]="Rehabilitation Officer|Environmental|Permanent|9 day fortnight|pilbara|740|20|4WD,WCARD,FA,C11"
  roles[++n]="Water Treatment Operator|Environmental|Casual|2:1 FIFO|pilbara|820|14|CSE,WCARD,FA,4WD"
  roles[++n]="Dust & Air Monitoring Tech|Environmental|Casual|Residential M-F|pilbara|650|12|4WD,WCARD,FA,EWP"
  roles[++n]="Waste Coordinator|Environmental|Permanent|2:1 FIFO|pilbara|780|8|HR,WCARD,FA,4WD"
  roles[++n]="Environmental Scientist|Environmental|Permanent|Residential M-F|perth|1120|6|4WD,WCARD,FA"
  roles[++n]="Labour Hire Pool (casual)|Recruitment|Labour Hire|2:1 FIFO|pilbara|540|38|WCARD,FA,C11"
  roles[++n]="Recruitment Consultant|Recruitment|Permanent|Residential M-F|perth|640|6|WCARD,FA"
  roles[++n]="Labour Hire Coordinator|Recruitment|Permanent|Residential M-F|perth|700|4|WCARD,FA"
  roles[++n]="Mobilisation Officer|Recruitment|Permanent|Residential M-F|perth|660|4|WCARD,FA"
  roles[++n]="HSE Advisor|Corporate|Permanent|2:1 FIFO|pilbara|1150|12|C11,WCARD,FA,CSE,WHT"
  roles[++n]="Rostering Coordinator|Corporate|Permanent|Residential M-F|perth|720|4|WCARD,FA"
  roles[++n]="People & Culture Advisor|Corporate|Permanent|Residential M-F|perth|860|6|WCARD,FA"
  roles[++n]="Payroll & Finance Officer|Corporate|Permanent|Residential M-F|perth|780|8|WCARD,FA"
  roles[++n]="Project Administrator|Corporate|Permanent|Residential M-F|perth|700|6|WCARD,FA"
  nroles=n

  split("Pilbara - Newman,Pilbara - Port Hedland,Pilbara - Karratha",psite,",")
  split("On Job,On Job,Available,Leave,On Job,Available",stt,",")

  id=48
  for (ri=1; ri<=nroles; ri++){
    m=split(roles[ri],p,"|")
    role=p[1]; sl=p[2]; et=p[3]; roster=p[4]; smode=p[5]; rate=p[6]; cnt=p[7]; sk=p[8]
    ns=split(sk,sa,",")
    for (k=1;k<=cnt;k++){
      id++
      first=fn[((id*7)%nf)+1]; last=ln[((id*13)%nl)+1]
      site=(smode=="perth")?"Perth - Applecross":psite[(id%3)+1]
      indig=((id%3==0)||(id%11==0))?"true":"false"
      status=stt[(id%6)+1]
      yr=2018+(id%8); mo=((id*5)%12)+1; dy=((id*3)%27)+1
      skills=""
      for(s=1;s<=ns;s++){ skills=skills (s>1?",":"") "\"" sa[s] "\"" }
      printf ",\n  {\n"
      printf "    \"employee_id\": \"EMP-%03d\",\n", id
      printf "    \"name\": \"%s %s\",\n", first, last
      printf "    \"role\": \"%s\",\n", role
      printf "    \"service_line\": \"%s\",\n", sl
      printf "    \"employment_type\": \"%s\",\n", et
      printf "    \"site\": \"%s\",\n", site
      printf "    \"roster\": \"%s\",\n", roster
      printf "    \"skills\": [%s],\n", skills
      printf "    \"indigenous\": %s,\n", indig
      printf "    \"status\": \"%s\",\n", status
      printf "    \"day_rate_aud\": %s,\n", rate
      printf "    \"start_date\": \"%04d-%02d-%02d\"\n", yr, mo, dy
      printf "  }"
    }
  }
}

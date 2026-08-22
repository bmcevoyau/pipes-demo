BEGIN {
  # ---- pools (deterministic, index-based; no RNG for reproducibility) ----
  nf = split("Jarrah,Kiara,Aden,Tanisha,Coen,Marlee,Djalu,Shanaya,Bailey,Ngaire,Tyrone,Leah,Corey,Amara,Dwayne,Talia,Kelton,Bindi,Rhys,Yindi,Marcus,Ellery,Kalarni,Brodie,Nerida,Jesse,Charmaine,Liam,Kirra,Owen,Shania,Declan,Mia,Blake,Alinta,Cody,Jedda,Noah,Warra,Ruby,Hayden,Lowanna,Jack,Tarni,Ethan,Kayleen,Sam,Dana",fn,",")
  nl = split("Nguyen,Bropho,Councillor,Ryan,Bennell,Hayes,Jetta,Little,Ugle,Walley,Yarran,Kelly,Michael,Dann,Garlett,Wynne,Champion,Farrell,Pickett,Riley,Stack,Roberts,Collard,Krakouer,Narkle,Blurton,Cameron,Comeagain,Egan,Hansen,Isaacs,Jones,Kickett,Miller,Ninyette,Oxenham,Penny,Quartermaine,Reibel,Smith,Taylor,Ugle,Valli,Winmar,Yappo,Abdullah,Baxter,Coyne",ln,",")

  # role | service_line | employment_type | roster | site(enum) | day_rate | skills(pipe)
  roles[1]="Trade Assistant|Industrial|Labour Hire|2:1 FIFO|Pilbara - Karratha|560|WHT|CSE|HR|C11|WCARD|FA"
  roles[2]="Plant Operator|Industrial|Permanent|8:6 FIFO|Pilbara - Newman|780|HR|C11|WCARD|4WD|FA"
  roles[3]="Boilermaker|Industrial|Permanent|2:1 FIFO|Pilbara - Tom Price|960|HR|CSE|WHT|C11|WCARD"
  roles[4]="Rigger / Dogger|Industrial|Permanent|2:1 FIFO|Pilbara - Karratha|1020|DOGRIG|WHT|CSE|C11|WCARD"
  roles[5]="Scaffolder|Industrial|Labour Hire|2:1 FIFO|Pilbara - Tom Price|900|WHT|C11|WCARD|FA"
  roles[6]="HD Diesel Fitter|Industrial|Permanent|8:6 FIFO|Pilbara - Newman|1080|HR|C11|WCARD|FA|4WD"
  roles[7]="Industrial Supervisor|Industrial|Permanent|2:1 FIFO|Pilbara - Karratha|1240|HR|C11|WCARD|FA|CSE"
  roles[8]="Blast/Vac Operator|Industrial|Casual|2:1 FIFO|Pilbara - Tom Price|720|CSE|WHT|WCARD|C11"
  roles[9]="Environmental Technician|Environmental|Permanent|9 day fortnight|Pilbara - Karratha|680|4WD|WCARD|FA|TM"
  roles[10]="Rehabilitation Officer|Environmental|Permanent|9 day fortnight|Pilbara - Newman|740|4WD|WCARD|FA|C11"
  roles[11]="Water Treatment Operator|Environmental|Permanent|2:1 FIFO|Pilbara - Tom Price|820|CSE|WCARD|FA|4WD"
  roles[12]="Dust & Air Monitoring Tech|Environmental|Labour Hire|Residential M-F|Pilbara - Karratha|650|4WD|WCARD|FA|EWP"
  roles[13]="Environmental Scientist|Environmental|Permanent|Residential M-F|Perth - Applecross|1120|4WD|WCARD|FA"
  roles[14]="Waste Coordinator|Environmental|Permanent|2:1 FIFO|Pilbara - Newman|780|HR|WCARD|FA|4WD"
  roles[15]="Recruitment Consultant|Recruitment|Permanent|Residential M-F|Perth - Applecross|640|WCARD|FA"
  roles[16]="Labour Hire Coordinator|Recruitment|Permanent|Residential M-F|Perth - Applecross|700|WCARD|FA"
  roles[17]="Mobilisation Officer|Recruitment|Permanent|Residential M-F|Perth - Applecross|660|WCARD|FA"
  roles[18]="HSE Advisor|Corporate|Permanent|2:1 FIFO|Pilbara - Karratha|1150|C11|WCARD|FA|CSE|WHT"
  roles[19]="Rostering Coordinator|Corporate|Permanent|Residential M-F|Perth - Applecross|720|WCARD|FA"
  roles[20]="People & Culture Advisor|Corporate|Permanent|Residential M-F|Perth - Applecross|860|WCARD|FA"
  nroles=20

  # status enum (schema): Available | On Job | Leave
  st[0]="On Job"; st[1]="On Job"; st[2]="Available"; st[3]="Leave"; st[4]="On Job"; st[5]="Available"; nst=6

  print "["
  N=48
  for (i=1;i<=N;i++){
    r=roles[((i-1)%nroles)+1]
    m=split(r,p,"|")
    role=p[1]; sl=p[2]; et=p[3]; roster=p[4]; site=p[5]; rate=p[6]
    skills=""
    for(c=7;c<=m;c++){ skills=skills (c>7?",":"") "\"" p[c] "\"" }
    first=fn[((i*7)%nf)+1]; last=ln[((i*13)%nl)+1]
    indig=((i%3==0)||(i%7==0))?"true":"false"
    status=st[i%nst]
    yr=2019+(i%7); mo=((i*5)%12)+1; dy=((i*3)%27)+1
    printf "  {\n"
    printf "    \"employee_id\": \"EMP-%03d\",\n", i
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
    printf "  }%s\n", (i<N?",":"")
  }
  print "]"
}

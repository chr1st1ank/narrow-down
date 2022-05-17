Search.setIndex({docnames:["api","apidoc/narrow_down.hash","apidoc/narrow_down.scylladb","apidoc/narrow_down.similarity_store","apidoc/narrow_down.sqlite","apidoc/narrow_down.storage","changelog","index","license","narrow_down","readme","user_guide/basic_usage","user_guide/configuration_of_indexing_and_search","user_guide/storage_backends"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":5,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":3,"sphinx.domains.rst":2,"sphinx.domains.std":2,"sphinx.ext.intersphinx":1,"sphinx.ext.viewcode":1,sphinx:56},filenames:["api.rst","apidoc/narrow_down.hash.rst","apidoc/narrow_down.scylladb.rst","apidoc/narrow_down.similarity_store.rst","apidoc/narrow_down.sqlite.rst","apidoc/narrow_down.storage.rst","changelog.md","index.rst","license.rst","narrow_down.rst","readme.md","user_guide/basic_usage.md","user_guide/configuration_of_indexing_and_search.md","user_guide/storage_backends.md"],objects:{"":[[9,0,0,"-","narrow_down"]],"narrow_down.hash":[[1,1,1,"","HashAlgorithm"],[1,3,1,"","murmur3_32bit"],[1,3,1,"","xxhash_32bit"],[1,3,1,"","xxhash_64bit"]],"narrow_down.hash.HashAlgorithm":[[1,2,1,"","Murmur3_32bit"],[1,2,1,"","Xxhash_32bit"],[1,2,1,"","Xxhash_64bit"]],"narrow_down.scylladb":[[2,1,1,"","ScyllaDBStore"]],"narrow_down.scylladb.ScyllaDBStore":[[2,4,1,"","__init__"],[2,4,1,"","add_document_to_bucket"],[2,4,1,"","initialize"],[2,4,1,"","insert_document"],[2,4,1,"","insert_setting"],[2,4,1,"","query_document"],[2,4,1,"","query_documents"],[2,4,1,"","query_ids_from_bucket"],[2,4,1,"","query_setting"],[2,4,1,"","remove_document"],[2,4,1,"","remove_id_from_bucket"]],"narrow_down.similarity_store":[[3,1,1,"","SimilarityStore"]],"narrow_down.similarity_store.SimilarityStore":[[3,4,1,"","create"],[3,4,1,"","insert"],[3,4,1,"","load_from_storage"],[3,4,1,"","query"],[3,4,1,"","query_top_n"],[3,4,1,"","remove_by_id"]],"narrow_down.sqlite":[[4,1,1,"","SQLiteStore"]],"narrow_down.sqlite.SQLiteStore":[[4,4,1,"","__init__"],[4,4,1,"","add_document_to_bucket"],[4,4,1,"","initialize"],[4,4,1,"","insert_document"],[4,4,1,"","insert_setting"],[4,4,1,"","query_document"],[4,4,1,"","query_documents"],[4,4,1,"","query_ids_from_bucket"],[4,4,1,"","query_setting"],[4,4,1,"","remove_document"],[4,4,1,"","remove_id_from_bucket"]],"narrow_down.storage":[[5,5,1,"","Fingerprint"],[5,1,1,"","InMemoryStore"],[5,1,1,"","StorageBackend"],[5,1,1,"","StorageLevel"],[5,1,1,"","StoredDocument"],[5,6,1,"","TooLowStorageLevel"]],"narrow_down.storage.InMemoryStore":[[5,4,1,"","__init__"],[5,4,1,"","add_document_to_bucket"],[5,4,1,"","deserialize"],[5,4,1,"","from_file"],[5,4,1,"","insert_document"],[5,4,1,"","insert_setting"],[5,4,1,"","query_document"],[5,4,1,"","query_ids_from_bucket"],[5,4,1,"","query_setting"],[5,4,1,"","remove_document"],[5,4,1,"","remove_id_from_bucket"],[5,4,1,"","serialize"],[5,4,1,"","to_file"]],"narrow_down.storage.StorageBackend":[[5,4,1,"","add_document_to_bucket"],[5,4,1,"","initialize"],[5,4,1,"","insert_document"],[5,4,1,"","insert_setting"],[5,4,1,"","query_document"],[5,4,1,"","query_documents"],[5,4,1,"","query_ids_from_bucket"],[5,4,1,"","query_setting"],[5,4,1,"","remove_document"],[5,4,1,"","remove_id_from_bucket"]],"narrow_down.storage.StorageLevel":[[5,2,1,"","Document"],[5,2,1,"","Fingerprint"],[5,2,1,"","Full"],[5,2,1,"","Minimal"]],"narrow_down.storage.StoredDocument":[[5,2,1,"","data"],[5,4,1,"","deserialize"],[5,2,1,"","document"],[5,2,1,"","exact_part"],[5,2,1,"","fingerprint"],[5,2,1,"","id_"],[5,4,1,"","serialize"],[5,4,1,"","without"]],narrow_down:[[1,0,0,"-","hash"],[2,0,0,"-","scylladb"],[3,0,0,"-","similarity_store"],[4,0,0,"-","sqlite"],[5,0,0,"-","storage"]]},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","attribute","Python attribute"],"3":["py","function","Python function"],"4":["py","method","Python method"],"5":["py","data","Python data"],"6":["py","exception","Python exception"]},objtypes:{"0":"py:module","1":"py:class","2":"py:attribute","3":"py:function","4":"py:method","5":"py:data","6":"py:exception"},terms:{"0":[3,11,12,13],"05":[3,12],"1":[1,5,12,13],"100":13,"128":4,"13":11,"2":[1,5,12],"20":11,"200":13,"2021":8,"24":11,"2x":6,"3":[3,11,12],"32":1,"4":[1,5,12],"42":11,"5":12,"6":12,"61":6,"62":6,"63":6,"64":1,"7":5,"75":[3,11,12],"9042":13,"abstract":13,"byte":[1,2,4,5,6],"case":[2,3,4,6,12,13],"class":[0,1,2,3,4,5,6,11,13],"default":[3,5,12,13],"do":[6,13],"enum":[1,5,13],"final":[12,13],"float":3,"function":[0,1,3,6,7,10,11],"import":[11,12,13],"int":[1,2,3,4,5],"n\u00b2":[7,10],"new":[2,3,4,5,6,13],"return":[2,3,4,5,11,12,13],"short":12,"static":5,"true":[3,11],A:[2,3,4,5,6,11,12,13],AND:13,AS:8,As:[6,11],But:[3,11,13],For:[2,13],IF:13,IS:8,If:[2,3,4,5,7,10,13],In:[2,3,4,5,7,10,12,13],It:[3,7,10,12,13],NOT:13,OF:8,OR:8,On:[12,13],That:11,The:[2,3,4,5,6,7,10,11,12,13],There:11,To:[11,12],WITH:13,With:[12,13],__init__:[2,3,4,5,6],_token:[3,12],abc:5,abl:13,abov:[3,12],accept:6,access:13,across:13,actual:[3,5,12,13],add:[2,4,5],add_document_to_bucket:[2,4,5],addit:[3,5,13],address:12,adher:6,advantag:13,after:13,again:[3,6,13],agre:8,aiosqlit:6,air:12,algorithm:[1,7,10,12],alia:5,all:[2,3,4,5,6,7,10,11,12,13],allow:[6,11,13],almost:12,alreadi:3,also:[3,5,6,7,10,11,12,13],although:12,amaz:11,amount:13,an:[2,3,4,5,6,7,8,10,11,13],ani:[2,4,5,8,11],anymor:13,anytim:11,anywai:6,apach:[2,13],api:[3,7,10,11,13],appli:[7,10,12],applic:[8,13],approach:[7,10],approxim:[7,10,12],ar:[3,6,11,12,13],argument:[6,13],articl:12,artifact:6,asn:12,assign:3,assum:3,async:[2,3,4,5],asynchron:[6,11,13],asyncio:[7,10,11],asyncsqlitestor:6,attribut:[5,13],autom:[7,10],automat:12,avail:[1,3,6,7,10,12,13],avoid:6,await:[11,12,13],awesom:11,backend:[2,3,4,5,6,7,10],bake:11,band:12,base:[1,2,3,4,5,6,7,10,12,13],basi:8,bear:12,becaus:[3,6,13],been:3,befor:[3,12],being:3,belong:[2,4,5],below:[11,12,13],benefici:12,benefit:6,bert:[7,10],better:[11,13],between:[11,12],beyond:13,binari:13,bit:[1,11],block:11,bodi:12,bomb:11,bool:3,both:[11,13],bound:13,boundari:13,box:13,broke:6,bucket:[2,4,5],bucket_id:[2,4,5],build:6,built:[3,13],c:[3,8,12,13],cach:13,calcul:[1,6,11,12,13],call:[6,11],callabl:3,can:[2,3,5,6,7,10,11,12,13],candid:3,cannot:[3,13],cardin:[7,10,12],care:[3,13],cassandra:[2,6,7,10],cassandra_clust:13,cassandra_storag:13,certain:[2,4,5],chain:11,chang:13,chapter:12,char_ngram:[3,6,11,12],charact:[3,6,11],check:6,check_if_exist:3,chewi:11,choic:[7,10,12],choos:11,chr1st1ank:[7,10],christian:8,ci:6,classic:[7,10],classmethod:[3,5],cluster:[2,13],cluster_or_sess:2,code:[11,13],collect:[3,6,7,10,12],com:[2,7,10],combin:5,comma:12,commit:13,common:[12,13],compar:[3,6,7,10],compat:2,complianc:8,concurr:[6,13],condens:12,condit:8,configur:[11,13],connect:[2,4,13],consumpt:[3,6,12],contact_point:13,contain:[6,12],content:5,continu:13,cooki:11,cookiecutt:[7,10],copi:[5,8],copyright:8,coroutin:[6,11],correct:3,corrupt:3,counter:6,coupl:12,cpu:12,creat:[2,3,4,5,6,7,10,11,12,13],current:[7,10],custom:3,cython:[7,10],dai:11,data:[2,3,4,5,6,7,10,11,13],data_typ:6,databas:[2,4,5,6,7,10,13],dataclass:13,dataset:[7,10,12],datasketch:[7,10],db:6,db_filenam:4,de:6,decreas:3,def:12,defin:[7,10,11,13],delici:11,deliou:11,demonstr:[11,12],depend:[6,12,13],describ:[6,12],descript:12,deseri:[3,5,6],design:13,detail:[2,5,13],detour:6,dictionari:6,differ:[3,6,7,10,11,12,13],direct:6,directli:[11,13],disadvantag:13,disk:[6,13],distinguish:5,distribut:[2,6,8,13],doc:[5,11],document:[2,3,4,5,6,7,10,12,13],document_hash:[2,4,5],document_id:[2,3,4,5,11],documentend:13,doe:[2,3,4,5],doesn:6,don:[7,10,12],done:[3,6],down:[9,12,13],driverexcept:2,dtype:5,durable_writ:13,e:[3,5,12,13],each:[3,7,10],easi:[7,10,13],economi:6,effect:[6,12,13],effici:13,effort:13,either:[8,13],element:3,elsewher:6,embed:[7,10],empti:[2,4,5,6,13],enabl:3,enough:13,enumer:11,especi:[11,13],establish:11,estim:[3,7,10,12],event:11,everi:[11,12,13],everyth:5,exact:[3,13],exact_part:[3,5,6,13],exactli:[3,5,13],exampl:[11,12,13],exce:13,except:[5,6,8],exchang:[7,10],execut:[11,13],exist:[2,3,4,5,6,13],expect:6,express:8,extens:[6,7,10],extern:13,extrem:12,f:12,factori:6,fail:[2,4],fairli:13,fals:[3,6,12,13],fast:[7,10,13],fastest:13,featur:5,fedejaur:[7,10],field:5,file:[2,4,5,6,8,13],file_path:5,fill:11,find:[3,6,7,10,12],fingerprint:[3,5,13],first:[6,11,13],flag:[1,5],flexibl:[7,10,13],flush:13,foil:11,follow:[12,13],footprint:[6,13],format:[6,13],forward:6,found:[2,3,4,5,12],frequent:12,from:[2,3,4,5,6,11,12],from_fil:[5,13],fu:12,full:[5,7,10,12,13],fulli:[6,11],further:12,fuss:11,fuz:12,fuzzi:[3,5,12,13],g:[3,5,12,13],gener:[1,12,13],get:[2,4,5,13],git:[7,10],github:[7,10],give:6,given:[2,3,4,5,12,13],good:[7,10,11],govern:8,grain:11,gram:[3,6,11],granular:3,great:[6,11],guarante:6,had:12,hair:12,hand:[12,13],handi:11,handl:12,happen:12,harder:12,hash:[0,2,4,5,6,7,10,12],hashalgorithm:1,have:[3,5,6,11,12,13],he:12,healthi:11,heavier:[7,10],here:11,heurist:12,high:[3,7,10],higher:[3,5,11,12],highli:[7,10],hold:13,home:11,homemad:11,how:[11,12,13],howev:3,http:[2,7,8,10],i:[11,12],id:[2,3,4,5,13],id_:[5,11,13],ident:[5,6],identifi:[2,3,4,5,13],implement:[5,6,7,10,13],impli:8,improv:6,incorrect:6,increas:6,increment:11,index:[3,6,7,10,13],inform:0,inherit:13,init:[3,6],initi:[2,3,4,5,6,13],inmemorystor:[5,6],input:[1,6,11,12,13],insert:[3,5,6,11,12,13],insert_docu:[2,4,5],insert_set:[2,4,5],instead:[6,13],integ:6,interest:[7,10],interfac:[5,7,10,13],intern:[3,5,6,12,13],invalid:2,io:[7,10],issu:6,item:[3,12],iter:[2,4,5],its:[2,4,5],itself:3,jaccard:[3,11,12],just:13,k:[7,10],keep:6,kei:[2,4,5,6],keyerror:[2,3,4,5],keyspac:[2,13],kid:11,kiddo:11,kind:[8,13],krudewig:8,languag:8,larg:[7,10,12],latenc:2,later:13,law:8,lead:[3,6],least:[2,3,4,5,11],leav:5,led:6,left:5,length:12,leskovec:12,less:12,let:12,level:[3,5,6,9,11,12],leverag:[6,13],lifetim:13,like:[3,6,7,10,12],limit:[6,8,13],line:13,linear:[7,10],link:[2,4,5],linux:13,list:[2,3,4,5,12],littl:11,load:3,load_from_storag:[3,13],local:[7,10,12,13],localhost:13,lock:6,longer:[6,12],look:12,loop:11,lot:[6,12],love:11,low:[2,3,12,13],lower:11,lsh:[6,7,10,12],lunchbox:11,mai:[3,8,12,13],make:[6,13],manag:13,massiv:12,match:[3,5,7,10,12,13],maturin:6,max_false_negative_proba:[3,12],max_false_positive_proba:[3,12],max_uint32:6,mean:11,mechan:3,memori:[3,6,7,10,12,13],messagepack:[5,6,13],method:[0,2,3,4,5,6,11,12,13],might:3,milvu:[7,10],mine:12,minhash:[5,6,7,10,12,13],minim:[3,5,13],minimum:[3,6,12],miss:3,modern:[7,10],modul:[0,7,10],modulo:6,more:[3,6,12,13],most:[3,6],mostli:13,move:6,msgpack:[5,13],multipl:[2,4,5,6,7,10,13],murmur3:1,murmur3_32bit:1,must:3,my:11,mypi:6,n:[3,6],name:[2,3,5,12,13],narrow:[9,12,13],narrow_down:[0,6,11,12,13],nativ:[7,10],nd:11,ndarrai:5,nearest:[7,10],necessari:[5,13],need:[3,5,7,10,13],neg:[3,12],neighbour:[7,10],newspap:12,ngram:3,none:[2,3,4,5,13],notabl:6,note:[3,13],noth:3,now:[6,11],number:[3,6,12],numpi:5,o:[7,10],oatmeal:11,object:[2,3,4,5,6,11,13],obtain:8,offer:[6,7,10,13],often:11,onc:6,one:[2,4,5,6,12,13],ones:12,onli:[3,5,6,7,10,13],oper:[5,6,13],operationalerror:4,optim:[6,7,10],option:[2,3,4,5,6,12,13],order:[3,6,13],org:8,origin:3,other:[3,7,10,11,12,13],otherwis:[3,6],out:[5,6,13],outsid:13,over:[11,13],overflow:6,overhead:11,packag:[0,7,10,11],packet:11,pad:[6,12],pair:[2,4,5,12],paramet:[2,3,4,5,6,7,10,12],pars:6,part:[3,13],partit:[4,6],pass:[3,12,13],path:5,payload:[3,5,13],peak:6,per:[3,13],perform:[5,6,7,10,13],permiss:8,permut:[6,12],persist:[3,5,13],phase:11,physic:13,pip:[7,10],plug:13,popular:11,port:13,posit:[3,6,12],possibl:[3,5,6,12,13],preced:6,predict:11,prefer:13,prefix:2,preprocess:11,prime:6,print:12,probabilist:3,probabl:[3,12],problem:[7,10],process:[3,12,13],produc:12,product:11,project:6,protobuf:6,protocol:2,purpos:1,pylsh:[7,10],pypackag:[7,10],pypi:6,python:[6,7,10],quaker:11,qualiti:6,queri:[2,3,4,5,6,12,13],query_docu:[2,4,5,6],query_ids_from_bucket:[2,4,5],query_set:[2,4,5],query_top_n:[3,6],quick:11,rais:[2,3,4,5],rajaraman:12,rather:[6,11,13],raw_str:12,re:[3,13],reach:12,readi:11,realiti:3,realli:3,reason:[2,4],reduc:[6,7,10],reimplement:13,releas:6,relev:11,reli:6,remov:[2,3,4,5],remove_by_id:[3,6],remove_docu:[2,4,5],remove_id_from_bucket:[2,4,5],reopen:13,replic:13,replication_factor:13,repo:[7,10],repres:[5,13],represent:12,requir:8,rest:13,result:[3,5,6,12,13],retriev:[3,13],reus:6,review:11,rich:[7,10],risk:3,row:12,run:[6,11],rust:[5,6,7,10],rustmemorystor:5,s:[1,12,13],same:[3,13],save:[3,6],scale:[6,7,10],scheme:[7,10],score:6,scylladb:[0,6,7,10],scylladbstor:[2,6,13],search:[3,5,11,13],search_result:11,second:13,section:11,see:[2,3,8,13],self:[2,4,5,6],semant:[6,12],sens:12,sensit:[7,10,12],sentenc:[5,12],serial:[5,6,13],serv:13,server:13,servic:13,session:[2,6,13],set:[2,3,4,5,6,13],setup:13,share:12,shorter:12,should:[3,5,12,13],show:[11,12,13],show_first:12,similar:[3,6,11,12],similarity_stor:[0,11,12,13],similarity_threshold:[3,11,12],similaritystor:[2,3,4,5,6,11,12],simpl:[11,13],simplest:13,simplestrategi:13,singl:13,size:13,sketch:[7,10],slow:13,slower:[3,13],small:[7,10],smaller:3,snack:11,so:[5,11,13],soft:11,some:[7,10,11,12,13],sometim:13,somewher:5,sourc:[1,2,3,4,5],specif:[0,8],specifi:[3,5],speed:6,speedup:6,split:[3,11,12],sqlite3:4,sqlite:[0,2,6,7,10],sqlitestor:[4,13],stack:[7,10],stapl:11,start:13,storag:[0,2,3,4,6,7,10,11],storage_backend:13,storage_level:[3,5,11,13],storagebackend:[2,3,4,5,13],storagelevel:[3,5,11,13],store:[2,3,4,5,6,11,12,13],storeddocu:[3,5,6,11],str:[2,3,4,5],straight:6,string:[1,2,3,4,5,7,10,12,13],strings_to_index:11,structur:[3,5,6,13],support:13,synchron:[6,11],system:[6,13],t:[6,7,10,12],tabl:[2,4,6,13],table_prefix:[2,6],take:[6,13],taken:3,target:[3,11,12],tast:11,templat:[7,10],test:6,test_k:13,text:[7,10,12,13],than:[3,6,13],thank:[7,10],thei:[3,5,12],them:11,themselv:3,therefor:[6,13],thi:[2,3,4,5,6,7,8,10,11,13],threshold:[3,11,12],thrown:6,time:[6,11,13],tmp:13,to_fil:[5,13],togeth:[3,5,13],token:[3,6,11],too:3,toolowstoragelevel:[3,5],top:[3,9],top_n_queri:6,total:11,train:11,tri:[6,12],tune:[7,10,12],turn:6,two:[3,12,13],type:[2,3,4,5,12],typeerror:[3,6],typehint:6,typic:13,uint32:5,ullman:12,under:[2,3,4,5,8],uniniti:[2,4,5],union:[2,3],uniqu:[12,13],unless:8,unprocess:5,unsupport:13,url:6,us:[2,3,5,6,7,8,10,11],usabl:[3,7,10],usag:[6,13],usecas:13,user:[6,7,10,13],uzzi:12,valid:[3,6],valu:[1,2,4,5,6,12,13],valueerror:[2,3],vector:[7,10],veri:[7,10,11,13],version:[6,8],via:6,w:12,wa:[2,3,4,5,6,7,10,12],wai:[6,12,13],want:11,warranti:8,wasn:12,we:[11,13],webpag:12,well:[7,10,11],were:6,when:[2,3,6,7,10,13],where:6,whether:3,which:[2,3,4,5,6,11,12,13],whole:[5,11,13],window:13,within:13,without:[5,6,8,11,12,13],word2vec:[7,10],word:[3,6],word_ngram:[3,12],work:[7,10,11],wors:6,wow:11,write:[6,8,13],wrong:6,wuzzi:12,www:[2,8],xxhash:1,xxhash_32bit:1,xxhash_64bit:1,y:12,you:[7,8,10],yum:11,yummi:11,zzy:12},titles:["API Documentation","narrow_down.hash module","narrow_down.scylladb module","narrow_down.similarity_store module","narrow_down.sqlite module","narrow_down.storage module","Changelog","Narrow Down - Efficient near-duplicate search","Apache Software License 2.0","narrow_down package","Narrow Down - Efficient near-duplicate search","Basic Usage","Configuration of Indexing and Search","Storage Backends"],titleterms:{"0":[6,8],"01":6,"02":6,"03":6,"04":6,"05":6,"06":6,"08":6,"09":6,"1":6,"10":6,"12":6,"13":6,"14":6,"16":6,"17":6,"2":[6,8],"2021":6,"2022":6,"23":6,"25":6,"29":6,"3":6,"30":6,"4":6,"5":6,"6":6,"7":6,"8":6,"9":6,"function":12,ad:[6,11],apach:8,api:0,backend:13,basic:11,cassandra:13,chang:6,changelog:6,charact:12,choos:12,configur:12,credit:[7,10],custom:[12,13],document:[0,11],down:[7,10],duplic:[7,10],effici:[7,10],explicitli:13,extra:[7,10],featur:[7,10],fix:6,from:13,gram:12,hash:1,index:[11,12],inmemorystor:13,instal:[7,10],level:13,licens:8,load:13,modul:[1,2,3,4,5],more:11,n:12,narrow:[7,10],narrow_down:[1,2,3,4,5,9],packag:9,precis:12,project:[7,10],queri:11,remov:6,right:12,scylladb:[2,13],search:[7,10,12],set:12,similar:[7,10],similarity_stor:3,similaritystor:13,softwar:8,specifi:13,sqlite:[4,13],storag:[5,13],storeddocu:13,token:12,unreleas:6,us:13,usag:11,word:12}})
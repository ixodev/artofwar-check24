proc noblehouseshield

messagebox; "Mr. Rich" ; "Only rich people are allowed here"; MESSAGEBOX_OK

endproc noblehouseshield

proc giantracoon;npc

facesetbox;"Giant Racoon";"RAAAAH!";(()getnpcname;npc);MESSAGEBOX_OK

endproc giantracoon

proc villager3;npc

facesetbox; "Villager" ;"You should visit this house. A rich man lives there.";(()getnpcname;npc);MESSAGEBOX_OK
facesetbox; "Villager" ;"Look at the magic!";(()getnpcname;npc);MESSAGEBOX_OK
fx_npc;npc;"Ice";2;1

endproc villager3

proc axolotl;npc
fx_npc;npc;"Smoke";1;3
endproc axolotl

proc fprincess;npc

facesetbox;"Princess Helen";"One day my prince will come...";(()getnpcname;npc);MESSAGEBOX_OK
facesetbox;"You";"I'm pretty sure that your prince does not exist.";(()getplayername);MESSAGEBOX_OK

endproc fprincess


proc fslime;npc
var i=()getnpcinteractions;npc

messagebox;"Slime";"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque semper, ex eget molestie finibus, neque nulla consectetur lacus, at mattis elit sapien in nunc. Suspendisse ac rutrum nisl. Sed rhoncus lectus erat, vitae accumsan diam fringilla in. Mauris consectetur lacus rhoncus, dignissim purus vel, elementum est. Curabitur sed erat quis arcu consectetur faucibus sed et diam. Maecenas vehicula enim vestibulum ipsum aliquet, eu placerat justo faucibus. Maecenas vel eleifend neque. Morbi non massa libero. Nunc quis ullamcorper sapien, non sagittis velit. Aliquam ultricies rhoncus pharetra. Curabitur lobortis tortor ligula, ac tempor orci commodo sed. Cras tincidunt, tortor eu dictum consequat, erat enim tincidunt nisl, in posuere augue mi in est. TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST"; MESSAGEBOX_OK
fx_npc;npc;"Plant";1;1

endproc fslime


proc noble;npc

var i=()getnpcinteractions;npc

if i==1 {
facesetbox;"The Rich Guy";"Hello! Welcome into my house! I suppose you are not as rich as me? Oh, and this is my wife!";(()getnpcname;npc);MESSAGEBOX_OK
}

else {
facesetbox;"The Rich Guy";"Oh you are here again! Did you get any money for me?";(()getnpcname;npc);MESSAGEBOX_OK
facesetbox;"You";"No.";(()getplayername);MESSAGEBOX_OK
}

endproc noble


proc noblewife;npc


var i=()getnpcinteractions;npc

if i==1 {
var res=()facesetbox;"The wife";"Have you ever heard of the old master?";(()getnpcname;npc);MESSAGEBOX_YES_NO
if res==MESSAGEBOX_OK_YES_STATUS {
facesetbox;"The wife";"You know where to find him? You should go to the library.";(()getnpcname;npc);MESSAGEBOX_OK
}
else {
facesetbox;"The wife";"He is a very old and wise man. You should go to the library.";(()getnpcname;npc);MESSAGEBOX_OK
}

facesetbox;"You";"Yeah, thanks!";(()getplayername);MESSAGEBOX_OK
ret
}

facesetbox;"The wife";"Oh, you are here again. What did the old master say to you?";(()getnpcname;npc);MESSAGEBOX_OK
facesetbox;"You";"Nothing really important.";(()getplayername);MESSAGEBOX_OK


endproc noblewife

proc petsnake2;npc
var i=()getnpcinteractions;npc

if i==1 {
#facesetbox;"You";"Let's see this snake...";(()getplayername);MESSAGEBOX_OK
fx_npc;npc;"Thunder";1;10
fx_wait
#facesetbox;"The Rich Guy";"Very funny, isn't it? It's our pet snake.";"Noble";MESSAGEBOX_OK
facesetbox;"You";"I do not find this joke very funny.";(()getplayername);MESSAGEBOX_OK
}
else {
facesetbox;"You";"I shouldn't touch him. Last time I became an electric shock.";(()getplayername);MESSAGEBOX_OK
}

endproc petsnake2


proc nobleeggboy;npc

facesetbox;"The son";"Look at this, I can do magic!";(()getnpcname;npc);MESSAGEBOX_OK
fx_npc;npc;"Plant";1;2

endproc nobleeggboy

proc libmaster;npc

var i=()getnpcinteractions;npc

if i==1 {

facesetbox;"You";"Hum... Hello?";(()getplayername);MESSAGEBOX_OK
facesetbox;"You";"Are you the old master?";(()getplayername);MESSAGEBOX_OK
facesetbox;"The Old Master";"Found him you just.";(()getnpcname;npc);MESSAGEBOX_OK
facesetbox;"You";"I am searching a diamond...";(()getplayername);MESSAGEBOX_OK
facesetbox;"The Old Master";"Oh oh oh... You shouldn't do it.";"Master";MESSAGEBOX_OK
}

else {
facesetbox;"The Old Master";"Are you here again to provoke me?";"Master";MESSAGEBOX_OK
}

endproc libmaster

proc liboldman;npc

facesetbox;"Old Man";"Hello!";(()getnpcname;npc);MESSAGEBOX_OK

endproc liboldman
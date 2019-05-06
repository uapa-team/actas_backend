from mongoengine import *

# Create your models here.
class Request(DynamicDocument):
    date = DateField()
    type = StringField(max_length=255)
    appr_status = ('Approved','Not approved','More') #We have more choises, TODO: write the missing ones 
    appr_stat = StringField(cmax_length=255, choices=appr_status) 
    stud_name = StringField(max_length=511)
    dni_types = ('Cédula', 'Pasaporte', 'More') #We have more choises, TODO: write the missing ones 
    stud_dni_type = StringField(choices=dni_types)
    stud_dni = StringField(max_length=22)
    acad_peri = StringField(max_length=10)
    cod_programs = ('VISI','2505','2541','2542','2544','2545','2546','2547','2548','2549','2879','BAPA','BAPC','BAPD','BAPE','BAPG','BAPH','BAPI','BAPM','BAPN','BAPO','BGCH','BGFA','BGFC','BGFD','BGFI','BGFM','2562','2577','2578','2698','2699','2700','2701','2702','2703','2704','2705','2706','2707','2708','2709','2710','2794','2856','2865','2882','2928','TGFI','2064','2113','2217','2278','2285','2573','2687','2691','2696','2792','2886','2896','2682','2683','2684','2685','2686','2838','2839','2880','2887')
    req_acad_prog = StringField(max_length=4, choices=cod_programs)
    req_just = StringField(max_length = 255)

class Test(DynamicDocument):
    hola = StringField()
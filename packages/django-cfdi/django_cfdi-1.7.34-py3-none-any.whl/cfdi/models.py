import requests, json, subprocess
from django.db import models
from .settings import (
    CFDI_DB_TABLE, XML_DIR, PRODIGIA_AUTH, TMP_DIR,
)

from django.contrib.auth.models import User


class Cfdi(models.Model):
    cfdi_xml = models.TextField()
    cfdi_error = models.TextField()
    cfdi_qrcode = models.TextField()
    acuse_cancelacion = models.TextField()
    cfdi_uuid = models.CharField(max_length=255, blank=True)
    cfdi_fecha_timbrado = models.DateTimeField(null=True)
    cfdi_sello_digital = models.TextField()
    cfdi_no_certificado_sat = models.TextField()
    cfdi_sello_sat = models.TextField()
    cadena_original_complemento = models.TextField()
    cfdi_status = models.TextField()
    inicio_conexion_pac = models.DateTimeField()
    fin_conexion_pac = models.DateTimeField()
    inicio_timbrado = models.DateTimeField()
    fin_timbrado = models.DateTimeField()
    folio = models.IntegerField(null=True)
    serie = models.CharField(max_length=10)
    tipo_comprobante = models.CharField(max_length=2)

    @property
    def xml(self):
        return self.cfdi_xml

    def cancelar_cfdi(self, config, timbrado_prueba=None, v33=False):
        from .functions import obtener_cancelacion_cfdi_base
        from .classes import CFDI
        if not self.cfdi_uuid:
            raise ValueError("El recibo no tiene UUID.")

        cfdi = obtener_cancelacion_cfdi_base(
            config, 
            uuid=self.cfdi_uuid,
            xml=self.cfdi_xml,
            timbrado_prueba=timbrado_prueba, 
        )
        cancelado, error_cancelacion = cfdi.cancelar_cfdi()
        if cancelado:
            self.cancelado = True
            self.acuse_cancelacion = cfdi.acuse_cancelacion
            self.save()

        return [cancelado, error_cancelacion]

    class Meta:
        db_table = CFDI_DB_TABLE


    def get_total_tiempo_timbrado(self):
        if self.inicio_conexion_pac and self.fin_conexion_pac and self.inicio_timbrado and self.fin_timbrado:
            dif_conexion = (self.fin_conexion_pac - self.inicio_conexion_pac)
            dif_timbrado = (self.fin_timbrado - self.inicio_timbrado)
            dif = dif_conexion + dif_timbrado
            return "%s.%06d" % (dif.seconds, dif.microseconds)

    def set_folio(self):
        if not self.folio:
            instance = self.__class__.objects.filter(
                tipo_comprobante=self.tipo_comprobante,
                serie=self.serie,
            ).order_by("-folio").first()

            self.folio = (instance.folio + 1) if instance else 1

    def xml_name(self):
        if self.cfdi_uuid:
            return "%s.xml" % self.cfdi_uuid

        return "%s.xml" % (self.folio or self.id)

    def get_xml_binary_file(self):
        return {
            'name':"%s.xml" % (self.cfdi_uuid),
            'data':self.cfdi_xml.encode("utf-8"),
            'content_type':"application/xml",
        }

    def xml_path(self, clave):
        import os
        d = "%s/%s" % (XML_DIR, clave)
        if not os.path.exists(d):
            os.makedirs(d)

        return "%s/%s" % (d, self.xml_name())

    def crear_xml_timbrado(self, clave="dmspitic"):
        import codecs
        f = open(self.xml_path(clave=clave), 'w')
        #f.write( codecs.BOM_UTF8 )
        try:
            f.write(self.cfdi_xml)
        except:
            f.write(self.cfdi_xml.encode('utf-8'))
        f.close()

    def generar_xml(self, cfdi):

        self.tipo_comprobante = cfdi.TipoDeComprobante
        self.serie = cfdi.Serie
        if cfdi.Folio:
            self.folio = cfdi.Folio
        else:
            self.set_folio()
            cfdi.Folio = self.folio

        cfdi.generar_xml_v33()
        error_sello = cfdi.generar_sello()
        if error_sello:
            self.cfdi_status = error_sello
            self.save()
            return 
        cfdi.sellar_xml()
        timbrado = cfdi.timbrar_xml()
        #Se Guardan los tiempos de timbrado
        self.inicio_conexion_pac = cfdi.inicio_conexion_pac
        self.fin_conexion_pac = cfdi.fin_conexion_pac
        self.inicio_timbrado = cfdi.inicio_timbrado
        self.fin_timbrado = cfdi.fin_timbrado

        if not timbrado:
            self.cfdi_status = cfdi.cfdi_status
            self.cfdi_xml = cfdi.xml
            self.save()
        else:
            self.cfdi_xml = cfdi.cfdi_xml
            self.cfdi_qrcode = cfdi.cfdi_qrcode
            self.cfdi_sello_digital = cfdi.cfdi_sello_digital
            self.cfdi_uuid = cfdi.cfdi_uuid
            self.cfdi_sello_sat = cfdi.cfdi_sello_sat
            self.cadena_original_complemento = cfdi.cadena_original_complemento
            self.cfdi_fecha_timbrado = cfdi.cfdi_fecha_timbrado
            self.cfdi_no_certificado_sat = cfdi.cfdi_no_certificado_sat
            self.save()




class DescargaCfdi(models.Model):
    creado = models.DateTimeField(auto_now_add=True)
    usuario_creado = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name="%(class)s_creados",
        on_delete=models.PROTECT,
    )

    modificado = models.DateTimeField(auto_now=True)
    rfc_emisor = models.TextField(default="")
    rfc_receptor = models.TextField(default="")
    rfc_solicitante = models.TextField()
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()

    respuesta_solicitud = models.TextField()
    numero_solicitud = models.TextField()
    status = models.IntegerField(choices=(
        (1, "Pendiente de enviar"),
        (2, "Pendiente de consultar"),
        (3, "Sigue pendiente"),
        (4, "Finalizado"),
    ), default=1)

    respuesta_consulta = models.TextField()
    paquetes = models.TextField()
    tipo_solicitud = models.CharField(max_length=255, default="CFDI")

    def get_lista_paquetes(self):
        #urls_paquete = []
        if not self.respuesta_solicitud:
            return []

        try:
            jsondata = json.loads(self.respuesta_consulta.split("|")[-1])
        except json.JSONDecodeError:
            return []

        return jsondata.get("paquetes", [])

        #return urls_paquete
        
    
    #cfdi_ultima_consulta = models.DateTimeField(null=True)


    def solicitar_descarga(self):
        
        

        if not self.rfc_solicitante:
            raise ValueError("El RFC solicitante está vacío")

        if not self.rfc_solicitante in [self.rfc_emisor, self.rfc_receptor]:
            raise ValueError("El RFC solicitante debe ser igual al RFC emisor o al RFC receptor")

        assert self.fecha_inicio
        assert self.fecha_final
        assert self.pfx_fiel
        assert self.password_fiel

        assert not self.numero_solicitud

        data = {
            "rfcSolicitante": self.rfc_solicitante,
            "fechaInicio": self.fecha_inicio.strftime("%Y-%m-%d"),
            "fechaFinal": self.fecha_final.strftime("%Y-%m-%d"),
            "tipoSolicitud":self.tipo_solicitud,
            "pfx":self.pfx_fiel,
            "password": self.password_fiel,
            "usuario": PRODIGIA_AUTH["prod"]["usuario"],
            "passPade": PRODIGIA_AUTH["prod"]["password"],
            "contrato": PRODIGIA_AUTH["prod"]["contrato_descarga_cfdi"],
        }

        if self.rfc_emisor:
            data["rfcEmisor"] = self.rfc_emisor

        if self.rfc_receptor:
            data["rfcReceptor"] = self.rfc_receptor

        response = requests.post(
            "https://descargamasiva.pade.mx/api/solicitud/generar/",
            json=data,
            verify=False,
        )
        #self.respuesta_solicitud = f"{str(data)}|{response.text}"
        self.respuesta_solicitud = f"{response.text}"

        if response.ok:
            jd = json.loads(response.text)
            self.numero_solicitud = jd["numeroSolicitud"]
        else:
            raise Exception(self.respuesta_solicitud)
        
        self.status = 2
        self.save()



    def solicitar_status_descarga(self):
        """
        Consulta el estatus de una solicitud de descarga
        """
        if not self.numero_solicitud:
            raise ValueError("No hay número de solicitud")

        data = {   
            "numeroSolicitud": self.numero_solicitud,
            "usuario": PRODIGIA_AUTH["prod"]["usuario"],
            "passPade": PRODIGIA_AUTH["prod"]["password"],
            "contrato": PRODIGIA_AUTH["prod"]["contrato_descarga_cfdi"],
        }

        response = requests.post(
            "https://descargamasiva.pade.mx/api/solicitud/estatus/",
            json=data,
            verify=False
        )
        
        self.respuesta_consulta = f"{response.text}"
        if response.ok:
            if self.get_lista_paquetes():
                self.status = 4
            else:
                self.status = 3

        self.save()


class CertificadoSello(models.Model):
    creado = models.DateTimeField(auto_now_add=True)
    numero = models.CharField(max_length=20, unique=True)
    rfc = models.CharField(max_length=13, default="")
    pem = models.TextField(default="")
    vigencia_inicio = models.DateField(null=True)
    vigencia_fin = models.DateField(null=True)
    
    def get_url_certificado(self):
        """
        Regresa la URL para descargar certificados del SAT a partir de un número
        de certificado

        >>> get_url_certificado("00001000000504204971")
        https://rdc.sat.gob.mx/rccf/000010/000005/04/20/49/00001000000504204971.cer
        """
        nc = self.numero
        url = "https://rdc.sat.gob.mx/rccf/"
        url += f"{nc[0:6]}/{nc[6:12]}/{nc[12:14]}/{nc[14:16]}/{nc[16:18]}/{nc}.cer" 
        return url


    def save_pem(self):

        cer_file_path = TMP_DIR + self.numero
        url = self.get_url_certificado()
        
        try:
            response = requests.get(url=url)
            assert response.ok
                
        except Exception as e:
            return f"Error al descargar el certificado de la siguiente URL: {url} | error:{e}"
        
        else:
            with open(cer_file_path, "wb") as tmpfile:
                tmpfile.write(response.content)


        cmd = f"openssl x509 -inform DER -in {cer_file_path} -text"
            
        try:
            out = subprocess.check_output(cmd.split()).decode("utf-8")
        except Exception as e:
            #functions.send_to_sentry(e)
            raise(e)

        else:
            certificado = out.split("-----BEGIN CERTIFICATE-----")[1].split("-----END CERTIFICATE-----")[0].replace('\n','')
            self.pem = certificado
            self.save()


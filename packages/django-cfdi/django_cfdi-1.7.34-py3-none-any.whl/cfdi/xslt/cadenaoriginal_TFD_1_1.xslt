<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:fn="http://www.w3.org/2005/xpath-functions" xmlns:cfdi="http://www.sat.gob.mx/cfd/3" xmlns:tfd="http://www.sat.gob.mx/TimbreFiscalDigital" version="1.0">
	<xsl:output method="text" version="1.0" encoding="UTF-8" indent="no"/>
	<xsl:template name="Requerido"><xsl:param name="valor"/>|<xsl:call-template name="ManejaEspacios"><xsl:with-param name="s" select="$valor"/></xsl:call-template></xsl:template>
	<xsl:template name="ManejaEspacios">
		<xsl:param name="s"/>
		<xsl:value-of select="normalize-space(string($s))"/>
  </xsl:template>
  <xsl:template match="/"><xsl:apply-templates select="./cfdi:Comprobante"/></xsl:template>
  <xsl:template match="cfdi:Comprobante"><xsl:apply-templates select="./cfdi:Complemento"/></xsl:template>
  <xsl:template match="cfdi:Complemento">|<xsl:apply-templates select="./tfd:TimbreFiscalDigital"/>||</xsl:template>
  <xsl:template match="tfd:TimbreFiscalDigital">
		<xsl:call-template name="Requerido">
			<xsl:with-param name="valor" select="./@Version"/>
		</xsl:call-template>
		<xsl:call-template name="Requerido">
			<xsl:with-param name="valor" select="./@UUID"/>
		</xsl:call-template>
		<xsl:call-template name="Requerido">
			<xsl:with-param name="valor" select="./@FechaTimbrado"/>
		</xsl:call-template>
		<xsl:call-template name="Requerido">
			<xsl:with-param name="valor" select="./@RfcProvCertif"/>
		</xsl:call-template>
		<xsl:call-template name="Requerido">
			<xsl:with-param name="valor" select="./@SelloCFD"/>
		</xsl:call-template>
		<xsl:call-template name="Requerido">
			<xsl:with-param name="valor" select="./@NoCertificadoSAT"/>
		</xsl:call-template>
	</xsl:template>
</xsl:stylesheet>
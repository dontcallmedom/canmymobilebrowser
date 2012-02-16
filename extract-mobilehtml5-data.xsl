<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns="http://www.w3.org/1999/xhtml" xmlns:html="http://www.w3.org/1999/xhtml" exclude-result-prefixes="html">

<xsl:output method="text" encoding="utf-8" />

<xsl:template match="/html:html">
  <xsl:text>{</xsl:text>
  <xsl:for-each select="//html:tbody//html:td[@class='feature'][html:h2]">
    <xsl:text>"</xsl:text><xsl:value-of select="html:h2"/><xsl:text>": {</xsl:text>
    <xsl:text>"ios_saf":</xsl:text>
    <xsl:call-template name="cani">
      <xsl:with-param name="col"  select="1"/>
    </xsl:call-template>
    <xsl:text>,"android":</xsl:text>
    <xsl:call-template name="cani">
      <xsl:with-param name="col"  select="2"/>
    </xsl:call-template>
    <xsl:text>,"blackberry":</xsl:text>
    <xsl:call-template name="cani">
      <xsl:with-param name="col"  select="4"/>
    </xsl:call-template>
    <xsl:text>,"ie":</xsl:text>
    <xsl:call-template name="cani">
      <xsl:with-param name="col"  select="8"/>
    </xsl:call-template>
    <xsl:text>,"opera":</xsl:text>
    <xsl:call-template name="cani">
      <xsl:with-param name="col"  select="9"/>
    </xsl:call-template>
    <xsl:text>,"firefox":</xsl:text>
    <xsl:call-template name="cani">
      <xsl:with-param name="col"  select="11"/>
    </xsl:call-template>
    <xsl:text>}</xsl:text>
    <xsl:if test="position()!=last()">
      <xsl:text>,</xsl:text>
    </xsl:if>
  </xsl:for-each>
  <xsl:text>}</xsl:text>
</xsl:template>

<xsl:template name="cani">
  <xsl:param name="col"/>
  <xsl:variable name="min_version" select="normalize-space(//html:table//html:td[.='Minimum version tested']/following-sibling::html:td[position()=$col])"/>
  <xsl:variable name="cell" select="following-sibling::html:td[position()=$col]"/>
  <xsl:choose>
    <xsl:when test="not($cell/html:img)">
      <xsl:text>0</xsl:text>
    </xsl:when>
    <xsl:when test="$cell/html:img and normalize-space($cell)=''">
      "<xsl:value-of select="$min_version"/>"
    </xsl:when>
    <xsl:when test="$cell/html:img and contains($cell, '+')">
      "<xsl:value-of select="normalize-space(substring-before($cell, '+'))"/>"
    </xsl:when>
    <xsl:otherwise>
      "<xsl:value-of select="$min_version"/>"
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>
</xsl:stylesheet>
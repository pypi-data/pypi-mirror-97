<?xml version="1.0" encoding="utf-8" ?>
<xsl:stylesheet version="1.0" xmlns="http://www.w3.org/1999/xhtml" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:imdi="http://www.mpi.nl/IMDI/Schema/IMDI" xmlns:folia="http://ilk.uvt.nl/folia" xmlns:exsl="http://exslt.org/common" xmlns:dc="http://purl.org/dc/elements/1.1/">

<xsl:param name="css"></xsl:param>

<xsl:output method="html" encoding="UTF-8" omit-xml-declaration="yes" doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN" doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" indent="yes" />

<xsl:strip-space elements="*" />


<xsl:variable name="folia_version" select="'2.0.2'" />
<xsl:variable name="version" select="'2.0.5'" />


<xsl:template match="/folia:FoLiA">
  <html>
   <xsl:comment>
       HTML generated from FoLiA input through folia2html.xsl v<xsl:value-of select="$version" /> for FoLiA v<xsl:value-of select="$folia_version" />. Note that this viewer is limited! It is client-side only and fully static (there is no scripting, interactive parts are pure CSS). This viewer won't scale well, don't use it for huge FoLiA documents. For a more powerful alternative for visualising and editing FoLiA, see FLAT: https://github.com/proycon/flat
   </xsl:comment>
  <xsl:if test="folia:metadata/folia:meta[@id='direction'] = 'rtl'">
      <!-- The trick to getting proper right-to-left support for languages such
           as Arabic, Farsi, Hebrew is to set metadata field 'direction' to 'rtl'.
           -->
      <xsl:attribute name="dir">rtl</xsl:attribute>
  </xsl:if>
  <head>
        <meta http-equiv="content-type" content="application/xhtml+xml; charset=utf-8"/>
        <meta name="generator" content="folia2html.xsl" />
        <xsl:choose>
            <xsl:when test="folia:metadata/folia:foreign-data/dc:title">
                <title><xsl:value-of select="folia:metadata/folia:foreign-data/dc:title" /></title>
            </xsl:when>
            <xsl:when test="folia:metadata//imdi:Session/imdi:Title">
                <title><xsl:value-of select="folia:metadata[@type='imdi']//imdi:Session/imdi:Title" /></title>
            </xsl:when>
            <xsl:when test="folia:metadata/folia:meta[@id='title']">
                <title><xsl:value-of select="folia:metadata/folia:meta[@id='title']" /></title>
            </xsl:when>
            <xsl:otherwise>
                <title><xsl:value-of select="@xml:id" /></title>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:choose>
            <xsl:when test="metadata/@src">
                <!-- metadata is external, include the link -->
                <meta name="metadata">
                    <xsl:attribute name="content">
                        <xsl:value-of select="metadata/@src" />
                    </xsl:attribute>
                </meta>
            </xsl:when>
            <xsl:otherwise>
                <!-- metadata inside folia document, try to propagate some
                     known fields -->
                <meta name="author">
                    <xsl:attribute name="content">
                        <xsl:choose>
                            <xsl:when test="folia:metadata/folia:foreign-data/dc:creator">
                                <xsl:value-of select="folia:metadata/folia:foreign-data/dc:title" />
                            </xsl:when>
                            <xsl:when test="folia:metadata/folia:foreign-data/dc:contributor">
                                <xsl:value-of select="folia:metadata/folia:foreign-data/dc:contributor" />
                            </xsl:when>
                            <xsl:when test="folia:metadata/folia:meta[@id='author']">
                                <xsl:value-of select="folia:metadata/folia:meta[@id='author']" />
                            </xsl:when>
                            <xsl:otherwise>unknown</xsl:otherwise>
                        </xsl:choose>
                    </xsl:attribute>
                </meta>
                <meta name="language">
                    <xsl:attribute name="content">
                        <xsl:choose>
                            <xsl:when test="folia:metadata/folia:foreign-data/dc:language">
                                <xsl:value-of select="folia:metadata/folia:foreign-data/dc:language" />
                            </xsl:when>
                            <xsl:when test="folia:metadata/folia:meta[@id='language']">
                                <xsl:value-of select="folia:metadata/folia:meta[@id='language']" />
                            </xsl:when>
                            <xsl:otherwise>unknown</xsl:otherwise>
                        </xsl:choose>
                    </xsl:attribute>
                </meta>
                <meta name="publisher">
                    <xsl:attribute name="content">
                        <xsl:choose>
                            <xsl:when test="folia:metadata/folia:foreign-data/dc:publisher">
                                <xsl:value-of select="folia:metadata/folia:foreign-data/dc:publisher" />
                            </xsl:when>
                            <xsl:when test="folia:metadata/folia:meta[@id='publisher']">
                                <xsl:value-of select="folia:metadata/folia:meta[@id='publisher']" />
                            </xsl:when>
                            <xsl:otherwise>unknown</xsl:otherwise>
                        </xsl:choose>
                    </xsl:attribute>
                </meta>
                <meta name="license">
                    <xsl:attribute name="content">
                        <xsl:choose>
                            <xsl:when test="folia:metadata/folia:foreign-data/dc:license">
                                <xsl:value-of select="folia:metadata/folia:foreign-data/dc:license" />
                            </xsl:when>
                            <xsl:when test="folia:metadata/folia:foreign-data/dc:rights">
                                <xsl:value-of select="folia:metadata/folia:foreign-data/dc:rights" />
                            </xsl:when>
                            <xsl:when test="folia:metadata/folia:meta[@id='license']">
                                <xsl:value-of select="folia:metadata/folia:meta[@id='license']" />
                            </xsl:when>
                            <xsl:when test="folia:metadata/folia:meta[@id='licence']">
                                <xsl:value-of select="folia:metadata/folia:meta[@id='licence']" />
                            </xsl:when>
                            <xsl:otherwise>unknown</xsl:otherwise>
                        </xsl:choose>
                    </xsl:attribute>
                </meta>
                <meta name="source">
                    <xsl:attribute name="content">
                        <xsl:choose>
                            <xsl:when test="folia:metadata/folia:foreign-data/dc:source">
                                <xsl:value-of select="folia:metadata/folia:foreign-data/dc:source" />
                            </xsl:when>
                            <xsl:when test="folia:metadata/folia:meta[@id='source']">
                                <xsl:value-of select="folia:metadata/folia:meta[@id='source']" />
                            </xsl:when>
                            <xsl:otherwise>unknown</xsl:otherwise>
                        </xsl:choose>
                    </xsl:attribute>
                </meta>
            </xsl:otherwise>
        </xsl:choose>
        <style type="text/css">
 				body {
					/*background: #222222;*/
					background: #b7c8c7;
					font-family: sans-serif;
					font-size: 12px;
					margin-bottom:240px;
				}

				div.text {
					width: 700px;
					margin-top: 50px;
					margin-left: auto;
					margin-right: auto;
					padding: 10px;
					padding-left: 50px;
					padding-right: 50px;
					background: white;
					border: 2px solid black;
                    <xsl:if test="folia:metadata/folia:meta[@id='direction'] = 'rtl'">
                        direction: rtl;
                    </xsl:if>
				}

				div.div {
                    padding-left: 0px;
					padding-top: 10px;
					padding-bottom: 10px;
				}

				#metadata {
					font-family: sans-serif;
					width: 700px;
					font-size: 90%;
					margin-left: auto;
					margin-right: auto;
					margin-top: 5px;
					margin-bottom: 5px;
					background: #b4d4d1; /*#FCFFD0;*/
					border: 1px solid #628f8b;
					width: 40%;
					padding: 5px;
				}
				#metadata table {
                    <xsl:choose>
                        <xsl:when test="folia:metadata/folia:meta[@id='direction'] = 'rtl'">
                            text-align: right;
                        </xsl:when>
                        <xsl:otherwise>
                            text-align: left;
                        </xsl:otherwise>
                    </xsl:choose>
				}

				#text {
					border: 1px solid #628f8b;
					width: 60%;
					max-width: 1024px;
					background: white;
					padding: 20px;
					padding-right: 100px;
					margin-top: 5px;
					margin-left: auto;
					margin-right: auto;
					color: #222;
				}
				.s {
					background: white;
					display: inline;
					border-left: 1px white solid;
					border-right: 1px white solid;
				}
				.s:hover {
					background: #e7e8f8;
					border-left: 1px blue solid;
					border-right: 1px blue solid;
				}
				.word {
					display: inline;
					color: black;
					position: relative;
					text-decoration: none;
                    cursor: pointer;
					z-index: 24;
                }
                .sh {
                    background: #f4f9ca;
                }
                .cor {
                    background: #f9caca;
                }
                .s:hover .sh {
					background: #cfd0ed;
                }
                .s:hover .cor {
					background: #cfd0ed;
                }
                .word:hover svg.bigtree {
                    position: fixed;
                    left: 0px;
                    margin: 0px;
                }

				#text {
					border: 1px solid #628f8b;
					width: 60%;
					max-width: 1024px;
					background: white;
					padding: 20px;
					padding-right: 100px;
					margin-top: 5px;
					margin-left: auto;
					margin-right: auto;
					color: #222;
				}

				.word {
					display: inline;
					color: black;
					position: relative;
					text-decoration: none;
					z-index: 24;
				}

				.t {
					display: inline;
					text-decoration: none;
					z-index: 24;
				}

				.word .attributes { display: none; font-size: 12px; font-weight: normal; }
				.word:hover {
					/*text-decoration: underline;*/
					z-index: 25;
				}
				.word:hover .t {
					background: #bfc0ed;
					text-decoration: underline;
				}

				.word:hover .attributes {
					display: block;
					position: absolute;
					width: 340px;
					font-size: 12px;
					left: 2em;
					top: 2em;
					background: #b4d4d1; /*#FCFFD0;*/
					opacity: 0.9; filter: alpha(opacity = 90);
					border: 1px solid #628f8b;
					padding: 5px;
					text-decoration: none !important;
                    text-align: left;
                    <xsl:if test="folia:metadata/folia:meta[@id='direction'] = 'rtl'">
                        direction: ltr;
                    </xsl:if>
				}
				.attributes dt {
					color: #254643;
					font-weight: bold;
				}
				.attributes dd {
					color: black;
					font-family: monospace;
				}
				.attributes .wordid {
					display: inline-block:
					width: 100%;
					font-size: 75%;
					color: #555;
					font-family: monospace;
					text-align: center;
				}
				.event {
					padding: 10px;
					border: 1px solid #4f7d87;
				}
                pre.gap {
                    width: 90%;
					padding: 5px;
                    border: 1px dashed #ddd;
                    white-space: pre-wrap;
				}
				span.attrlabel {
					display: inline-block;
					color: #254643;
					font-weight: bold;
					width: 110px;
				}
				span.attrvalue {
					font-weight: 12px;
					font-family: monospace;
                }
                span.class {
                    color: #000099;
                    text-weight: bold;
                }
                span.morpheme {
                    font-style: italic;
                }
                span.details {
                    font-style: normal;
                    font-size: 80%;
                }

                div.caption {
                    text-align: center;
                    style: italic;
                }


				div#iewarning {
					width: 90%;
					padding: 10px;
					color: red;
					font-size: 16px;
					font-weight: bold;
					text-align: center;
				}
                td {
                 border: 1px solid #ddd;
                }

                thead {
                    font-weight: bold;
                    background: #ddd;
                }

                div.note {
                    font-size: 80%;
                    border-bottom: 1px #ddd dotted;
                }

                dl.entry {
                    border: 1px #aaa solid;
                    background: #ddd;
                    padding: 10px;
                }
                dt {
                    font-weight: bold;
                }
                dd.example {
                    font-style: italic;
                }
        </style>
        <xsl:if test="$css">
        <link rel="stylesheet">
            <xsl:attribute name="href"><xsl:value-of select="$css" /></xsl:attribute>
        </link>
        </xsl:if>
  </head>
    <body>
    	<xsl:comment><![CDATA[[if lte IE 10]>
		<div id="iewarning">
			The FoLiA viewer does not work properly with Internet Explorer, please consider upgrading to Mozilla Firefox or Google Chrome instead.
		</div>
		<![endif]]]></xsl:comment>
        <xsl:apply-templates />
    </body>
  </html>
</xsl:template>

<xsl:template match="folia:meta">
    <!-- ignore -->
</xsl:template>

<xsl:template match="folia:text">
 <div class="text">
    <xsl:if test="folia:feat"><xsl:attribute name="class"><xsl:call-template name="feat_to_css" /></xsl:attribute></xsl:if>
 	<xsl:apply-templates />
 </div>
</xsl:template>

<xsl:template match="folia:div">
 <div class="div">
   <xsl:if test="folia:feat"><xsl:attribute name="class"><xsl:call-template name="feat_to_css" /></xsl:attribute></xsl:if>
   <xsl:apply-templates />
 </div>
</xsl:template>

<xsl:template match="folia:p">
 <p id="{@xml:id}">
    <xsl:if test="folia:feat"><xsl:attribute name="class"><xsl:call-template name="feat_to_css" /></xsl:attribute></xsl:if>
    <xsl:apply-templates />
 </p>
</xsl:template>


<xsl:template match="folia:gap">
 <pre class="gap">
  <xsl:value-of select="folia:content" />
 </pre>
</xsl:template>


<xsl:template match="folia:head">
<xsl:choose>
 <xsl:when test="count(ancestor::folia:div) = 1">
    <h1>
        <xsl:call-template name="headinternal" />
    </h1>
 </xsl:when>
 <xsl:when test="count(ancestor::folia:div) = 2">
    <h2>
        <xsl:call-template name="headinternal" />
    </h2>
 </xsl:when>
 <xsl:when test="count(ancestor::folia:div) = 3">
    <h3>
        <xsl:call-template name="headinternal" />
    </h3>
 </xsl:when>
 <xsl:when test="count(ancestor::folia:div) = 4">
    <h4>
        <xsl:call-template name="headinternal" />
    </h4>
 </xsl:when>
 <xsl:when test="count(ancestor::folia:div) = 5">
    <h5>
        <xsl:call-template name="headinternal" />
    </h5>
 </xsl:when>
 <xsl:otherwise>
    <h6>
        <xsl:call-template name="headinternal" />
    </h6>
 </xsl:otherwise>
</xsl:choose>
</xsl:template>

<xsl:template name="headinternal">
    <span id="{@xml:id}" class="head">
        <xsl:attribute name="class">head<xsl:call-template name="feat_to_css" /></xsl:attribute>
        <xsl:apply-templates />
    </span>
</xsl:template>


<xsl:template match="folia:entry">
<dl class="entry">
    <xsl:if test="folia:feat"><xsl:attribute name="class"><xsl:call-template name="feat_to_css" /></xsl:attribute></xsl:if>
    <xsl:apply-templates />
</dl>
</xsl:template>

<xsl:template match="folia:term">
<dt>
    <xsl:if test="folia:feat"><xsl:attribute name="class"><xsl:call-template name="feat_to_css" /></xsl:attribute></xsl:if>
    <xsl:apply-templates />
</dt>
</xsl:template>

<xsl:template match="folia:def">
<dd>
    <xsl:if test="folia:feat"><xsl:attribute name="class"><xsl:call-template name="feat_to_css" /></xsl:attribute></xsl:if>
    <xsl:apply-templates />
</dd>
</xsl:template>

<xsl:template match="folia:ex">
<dd class="example">
    <xsl:if test="folia:feat"><xsl:attribute name="class"><xsl:call-template name="feat_to_css" /></xsl:attribute></xsl:if>
    <xsl:apply-templates />
</dd>
</xsl:template>

<xsl:template match="folia:list">
<ul>
    <xsl:if test="folia:feat"><xsl:attribute name="class"><xsl:call-template name="feat_to_css" /></xsl:attribute></xsl:if>
    <xsl:apply-templates />
</ul>
</xsl:template>

<xsl:template match="folia:item">
    <li><xsl:if test="folia:feat"><xsl:attribute name="class"><xsl:call-template name="feat_to_css" /></xsl:attribute></xsl:if><xsl:apply-templates /></li>
</xsl:template>

<xsl:template match="folia:note">
<div class="note">
    <a name="ref.{@xml:id}"></a>
    <xsl:apply-templates />
</div>
</xsl:template>

<xsl:template match="folia:ref">
    <xsl:choose>
    <xsl:when test="*">
        <xsl:apply-templates />
    </xsl:when>
    <xsl:otherwise>
    <!-- No child elements -->
    <a href="#ref.{@id}">*</a>
    </xsl:otherwise>
    </xsl:choose>
</xsl:template>


<xsl:template match="folia:s">
    <span id="{@xml:id}">
        <xsl:attribute name="class">s<xsl:call-template name="feat_to_css" /></xsl:attribute>
        <xsl:apply-templates />
    </span>
</xsl:template>

<xsl:template match="folia:part">
    <span class="part"><xsl:apply-templates /></span>
</xsl:template>

<xsl:variable name="ancestors_ok">not(ancestor::folia:original) and not(ancestor::folia:suggestion) and not(ancestor::folia:alt) and not(ancestor::folia:altlayers)</xsl:variable><!-- Checks if all ancestors are authoritative -->
<xsl:variable name="ancestors_nosubtoken">not(ancestor::folia:morpheme) and not(ancestor::folia:phoneme)</xsl:variable><!-- Checks if all ancestors are authoritative -->
<xsl:variable name="textclass_current">(not(@class) or (@class='current'))</xsl:variable>

<xsl:template match="folia:w">
    <xsl:variable name="wid" select="@xml:id" />
    <xsl:if test="$ancestors_ok">
        <span id="{@xml:id}"><xsl:attribute name="class">word<xsl:if test="//folia:wref[@id=$wid and not(ancestor::folia:altlayers)]"> sh</xsl:if><xsl:if test=".//folia:correction or .//folia:errordetection"> cor</xsl:if></xsl:attribute><span class="t"><xsl:value-of select="string(.//folia:t[$ancestors_ok and $ancestors_nosubtoken and not(ancestor::folia:str) and (not(@class) or @class = 'current')])"/></span><xsl:call-template name="inlineannotations" /></span>
    <xsl:choose>
       <xsl:when test="@space = 'no'"></xsl:when>
       <xsl:otherwise>
        <xsl:text> </xsl:text>
       </xsl:otherwise>
    </xsl:choose>
    </xsl:if>
</xsl:template>




<xsl:template match="folia:t">
    <!-- Test presence of text in deeper structure elements, if they exist we don't
         render this text but rely on the text in the deeper structure  -->
    <!-- Next, check if text element is authoritative (ancestors_ok) and have the proper class -->
    <xsl:if test="not(following-sibling::*//folia:t[$textclass_current and $ancestors_ok and $ancestors_nosubtoken and not(ancestor::folia:str)])"><xsl:if test="$textclass_current and $ancestors_ok and $ancestors_nosubtoken and not(ancestor::folia:str)"><xsl:apply-templates /></xsl:if></xsl:if>
</xsl:template>


<xsl:template match="folia:desc">
    <!-- ignore -->
</xsl:template>

<xsl:template match="folia:t-style">
    <!-- guess class names that may be indicative of certain styles,
         these are **NOT** defined by FoLiA, we're unaware of any sets here -->
    <xsl:choose>
    <xsl:when test="@class = 'bold' or @class = 'b'">
        <b><xsl:apply-templates /></b>
    </xsl:when>
    <xsl:when test="@class = 'italic' or @class = 'i' or @class = 'italics'">
        <i><xsl:apply-templates /></i>
    </xsl:when>
    <xsl:when test="@class = 'strong'">
        <strong><xsl:apply-templates /></strong>
    </xsl:when>
    <xsl:when test="@class = 'superscript'">
        <sup><xsl:apply-templates /></sup>
    </xsl:when>
    <xsl:when test="@class = 'subscript'">
        <sub><xsl:apply-templates /></sub>
    </xsl:when>
    <xsl:when test="@class = 'em' or @class = 'emph' or @class = 'emphasis'">
        <em><xsl:apply-templates /></em>
    </xsl:when>
    <xsl:otherwise>
        <span><xsl:attribute name="class">style_<xsl:choose><xsl:when test="@class"><xsl:value-of select="translate(normalize-space(@class), ' .{}[]#+=\@/,', '')" /></xsl:when><xsl:otherwise>none</xsl:otherwise></xsl:choose><xsl:for-each select="folia:feat"><xsl:text> style_</xsl:text><xsl:value-of select="@subset" />_<xsl:value-of select="translate(normalize-space(@class), ' .{}[]#+=\@/,', '')" /></xsl:for-each></xsl:attribute><xsl:apply-templates /></span>
    </xsl:otherwise>
    </xsl:choose>
</xsl:template>


<xsl:template name="feat_to_css"><xsl:if test="folia:feat"><xsl:for-each select="folia:feat"><xsl:text> feat_</xsl:text><xsl:value-of select="@subset" />_<xsl:value-of select="translate(normalize-space(@class), ' .{}[]#+=\@/,', '')" /></xsl:for-each></xsl:if></xsl:template>


<xsl:template match="folia:t-str">
    <xsl:choose>
        <xsl:when test="@xlink:href and @class">
            <a href="{@xlink:href}"><span class="str_{@class}"><xsl:apply-templates /></span></a>
        </xsl:when>
        <xsl:when test="@xlink:href">
            <a href="{@xlink:href}"><span class="str"><xsl:apply-templates /></span></a>
        </xsl:when>
        <xsl:when test="@class">
            <span class="str_{@class}"><xsl:apply-templates /></span>
        </xsl:when>
        <xsl:otherwise>
            <span class="str"><xsl:apply-templates /></span>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<xsl:template match="folia:t-gap">
    <span class="gap"><xsl:apply-templates /></span>
</xsl:template>


<xsl:template name="contentannotation_text">
    <xsl:if test="folia:t">
            <xsl:for-each select="folia:t">
                <span class="attrlabel">Text
                <xsl:if test="count(../folia:t) &gt; 1">
                    (<xsl:value-of select="@class" />)
                  </xsl:if>
                </span><span class="attrvalue"><xsl:value-of select=".//text()" /></span><br />
            </xsl:for-each>
      </xsl:if>
</xsl:template>

<xsl:template name="contentannotation_phon">
    <xsl:if test="folia:ph">
            <xsl:for-each select="folia:ph">
                <span class="attrlabel">Phonetics
                <xsl:if test="count(../folia:ph) &gt; 1">
                    (<xsl:value-of select="@class" />)
                  </xsl:if>
                </span><span class="attrvalue"><xsl:value-of select=".//text()" /></span><br />
            </xsl:for-each>
      </xsl:if>
</xsl:template>



<xsl:template name="inlineannotations">
 <span class="attributes">
     <span class="attrlabel">ID</span><span class="attrvalue"><xsl:value-of select="@xml:id" /></span><br />
        <xsl:call-template name="contentannotation_text" />
        <xsl:call-template name="contentannotation_phon" />
        <xsl:if test=".//folia:pos">
            <xsl:for-each select=".//folia:pos[$ancestors_ok and $ancestors_nosubtoken]">
            	<span class="attrlabel">PoS</span><span class="attrvalue class"><xsl:value-of select="@class" /></span><br />
            </xsl:for-each>
        </xsl:if>
        <xsl:if test=".//folia:lemma">
            <xsl:for-each select=".//folia:lemma[$ancestors_ok and $ancestors_nosubtoken]">
			    <span class="attrlabel">Lemma</span><span class="attrvalue class"><xsl:value-of select="@class" /></span><br />
            </xsl:for-each>
        </xsl:if>
        <xsl:if test=".//folia:sense">
            <xsl:for-each select=".//folia:sense[$ancestors_ok and $ancestors_nosubtoken]">
			    <span class="attrlabel">Sense</span><span class="attrvalue class"><xsl:value-of select="@class" /></span><br />
            </xsl:for-each>
        </xsl:if>
        <xsl:if test=".//folia:subjectivity[$ancestors_ok and $ancestors_nosubtoken]">
            <!-- This is a deprecated element!!! -->
            <xsl:for-each select=".//folia:subjectivity">
			    <span class="attrlabel">Subjectivity</span><span class="attrvalue class"><xsl:value-of select="@class" /></span><br />
            </xsl:for-each>
        </xsl:if>
        <xsl:if test=".//folia:metric">
            <xsl:for-each select=".//folia:metric[$ancestors_ok and $ancestors_nosubtoken]">
                <span class="attrlabel">Metric <xsl:value-of select="@class" /></span><span class="attrvalue"><xsl:value-of select="@value" /></span><br />
            </xsl:for-each>
        </xsl:if>
        <xsl:if test=".//folia:errordetection">
            <!-- This is a deprecated element!!! -->
            <xsl:for-each select=".//folia:errordetection[$ancestors_ok and $ancestors_nosubtoken]">
                <span class="attrlabel">Error detected</span><span class="attrvalue"><xsl:value-of select="@class" /></span><br />
            </xsl:for-each>
        </xsl:if>
        <xsl:if test="folia:correction">
            <!-- TODO: Expand to support all inline annotations -->
            <xsl:if test="folia:correction/folia:suggestion/folia:t">
            	<span class="attrlabel">Suggestion(s) for text correction</span><span class="attrvalue"><xsl:for-each select="folia:correction/folia:suggestion/folia:t">
                    <em><xsl:value-of select="." /></em><xsl:text> </xsl:text>
                </xsl:for-each></span><br />
            </xsl:if>
            <xsl:if test="folia:correction/folia:original/folia:t">
            	<span class="attrlabel">Original pre-corrected text</span>
            	<span class="attrvalue">
                <xsl:for-each select="folia:correction/folia:original/folia:t">
                    <em><xsl:value-of select="." /></em><xsl:text> </xsl:text>
                </xsl:for-each>
                </span><br />
            </xsl:if>
        </xsl:if>
        <xsl:if test=".//folia:morphology">
            <xsl:for-each select=".//folia:morphology[$ancestors_ok]">
                <span class="attrlabel">Morphology</span>
                <span class="attrvalue">
                    <xsl:for-each select="folia:morpheme">
                        <span class="morpheme">
                            <xsl:value-of select="./folia:t[$textclass_current]" />
                            <xsl:if test="@class">
                                <span class="details">(<xsl:value-of select="@class" />)</span>
                            </xsl:if>
                            <xsl:if test="@function">
                                <span class="details">[function=<xsl:value-of select="@function" />]</span>
                            </xsl:if>
                            <xsl:if test=".//folia:pos">
                                <xsl:for-each select=".//folia:pos[$ancestors_ok]">
                                    <span class="details">[pos=<xsl:value-of select="@class" />]</span>
                                </xsl:for-each>
                            </xsl:if>
                            <xsl:if test=".//folia:lemma">
                                <xsl:for-each select=".//folia:lemma[$ancestors_ok]">
                                    <span class="details">[lemma=<xsl:value-of select="@class" />]</span>
                                </xsl:for-each>
                            </xsl:if>
                            <xsl:text> </xsl:text>
                        </span>
                    </xsl:for-each>
                </span><br />
            </xsl:for-each>
        </xsl:if>
        <span class="spanannotations">
            <xsl:call-template name="spanannotations">
                <xsl:with-param name="id" select="@xml:id" />
            </xsl:call-template>
        </span>
 </span>
</xsl:template>


<xsl:template name="span">
    <xsl:param name="id" />
    <xsl:text> </xsl:text>
    <span class="span">
        <xsl:for-each select=".//folia:wref">
            <xsl:variable name="wrefid" select="@id" />
            <xsl:choose>
                <xsl:when test="@t">
                    <xsl:value-of select="@t" />
                    <xsl:text> </xsl:text>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:if test="//folia:w[@xml:id=$wrefid]">
                        <xsl:value-of select="//folia:w[@xml:id=$wrefid]/folia:t[$ancestors_ok]"/>
                    </xsl:if>
                    <xsl:text> </xsl:text>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:for-each>
    </span>
</xsl:template>

<xsl:template name="spanannotations">
    <xsl:param name="id" />

    <xsl:variable name="entities" select="ancestor::*"></xsl:variable>
    <xsl:for-each select="$entities">
        <xsl:for-each select="folia:entities">
            <xsl:for-each select="folia:entity">
                <xsl:if test=".//folia:wref[@id=$id]">
                    <span class="attrlabel">Entity</span>
                    <span class="attrvalue">
                        <span class="class"><xsl:value-of select="@class" /></span>
                        <xsl:call-template name="span">
                            <xsl:with-param name="id" select="$id" />
                        </xsl:call-template>
                    </span><br />
                </xsl:if>
            </xsl:for-each>
        </xsl:for-each>
    </xsl:for-each>

    <xsl:variable name="observations" select="ancestor::*"></xsl:variable>
    <xsl:for-each select="$observations">
        <xsl:for-each select="folia:observation">
            <xsl:for-each select="folia:observation">
                <xsl:if test=".//folia:wref[@id=$id]">
                    <span class="attrlabel">Observation</span>
                    <span class="attrvalue">
                        <span class="class"><xsl:value-of select="@class" /></span>
                        <xsl:call-template name="span">
                            <xsl:with-param name="id" select="$id" />
                        </xsl:call-template>
                    </span><br />
                </xsl:if>
            </xsl:for-each>
        </xsl:for-each>
    </xsl:for-each>


    <xsl:variable name="ancestors" select="ancestor::*"></xsl:variable>

    <xsl:for-each select="$ancestors">
    <xsl:for-each select="folia:chunking">
        <xsl:for-each select="folia:chunk">
            <xsl:if test=".//folia:wref[@id=$id]">
                <span class="attrlabel">Chunk</span>
                <span class="attrvalue">
                    <span class="class"><xsl:value-of select="@class" /></span>
                        <xsl:call-template name="span">
                            <xsl:with-param name="id" select="$id" />
                        </xsl:call-template>
                </span><br/>
            </xsl:if>
        </xsl:for-each>
    </xsl:for-each>
    </xsl:for-each>



    <xsl:for-each select="$ancestors">
    <xsl:for-each select="folia:semroles">
        <xsl:for-each select="folia:semrole">
            <xsl:if test=".//folia:wref[@id=$id]">
                <span class="attrlabel">Semantic Role</span>
                <span class="attrvalue">
                    <span class="class"><xsl:value-of select="@class" /></span>
                        <xsl:call-template name="span">
                            <xsl:with-param name="id" select="$id" />
                        </xsl:call-template>
                </span><br />
            </xsl:if>
        </xsl:for-each>
    </xsl:for-each>
    </xsl:for-each>


    <xsl:for-each select="$ancestors">
    <xsl:for-each select="folia:coreferences">
        <xsl:for-each select="folia:coreferencechain">
            <xsl:if test=".//folia:wref[@id=$id]">
                <span class="attrlabel">Coreference Chain</span>
                <span class="attrvalue">
                    <span class="class"><xsl:value-of select="@class" /></span>
                    <xsl:for-each select="folia:coreferencelink">
                        <xsl:call-template name="span">
                            <xsl:with-param name="id" select="$id" />
                        </xsl:call-template>
                        <xsl:text> - </xsl:text>
                    </xsl:for-each>
                    <br />
                </span><br/>
            </xsl:if>
        </xsl:for-each>
    </xsl:for-each>
    </xsl:for-each>

    <xsl:for-each select="$ancestors">
    <xsl:for-each select="folia:dependencies">
        <xsl:for-each select="folia:dependency">
            <xsl:if test=".//folia:wref[@id=$id]">
                <span class="attrlabel">Dependency</span>
                <span class="attrvalue">
                    <span class="class"><xsl:value-of select="@class" /></span><xsl:text> </xsl:text>
                        <xsl:for-each select="folia:hd">
                            <strong>Head:</strong>
                            <xsl:call-template name="span">
                                <xsl:with-param name="id" select="$id" />
                            </xsl:call-template>
                        </xsl:for-each>
                        <xsl:for-each select="folia:dep">
                            <strong>Dep:</strong>
                            <xsl:call-template name="span">
                                <xsl:with-param name="id" select="$id" />
                            </xsl:call-template>
                        </xsl:for-each>
                </span><br />
            </xsl:if>
        </xsl:for-each>
    </xsl:for-each>
    </xsl:for-each>

    <xsl:for-each select="$ancestors">
    <xsl:for-each select="folia:syntax">
        <span class="attrlabel">Syntax</span>
        <span class="attrvalue">
            <xsl:call-template name="su2svg">
                <xsl:with-param name="id" select="$id" />
            </xsl:call-template>
        </span><br/>
    </xsl:for-each>
    </xsl:for-each>

    <xsl:for-each select="$ancestors">
    <xsl:for-each select="folia:statements">
        <xsl:for-each select="folia:statement">
            <xsl:if test=".//folia:wref[@id=$id]">
                <span class="attrlabel">Statement</span>
                <span class="attrvalue">
                    <span class="class"><xsl:value-of select="@class" /></span><xsl:text> </xsl:text>
                        <xsl:for-each select="folia:hd">
                            <strong>Head:</strong>
                            <xsl:call-template name="span">
                                <xsl:with-param name="id" select="$id" />
                            </xsl:call-template>
                        </xsl:for-each>
                        <xsl:for-each select="folia:source">
                            <strong>Source:</strong>
                            <xsl:call-template name="span">
                                <xsl:with-param name="id" select="$id" />
                            </xsl:call-template>
                        </xsl:for-each>
                        <xsl:for-each select="folia:rel">
                            <strong>Relation:</strong>
                            <xsl:call-template name="span">
                                <xsl:with-param name="id" select="$id" />
                            </xsl:call-template>
                        </xsl:for-each>
                </span><br />
            </xsl:if>
        </xsl:for-each>
    </xsl:for-each>
    </xsl:for-each>


    <xsl:for-each select="$ancestors">
    <xsl:for-each select="folia:sentiments">
        <xsl:for-each select="folia:sentiment">
            <xsl:if test=".//folia:wref[@id=$id]">
                <span class="attrlabel">Sentiment</span>
                <span class="attrvalue">
                    <span class="class"><xsl:value-of select="@class" /></span><xsl:text> </xsl:text>
                        <xsl:for-each select="folia:hd">
                            <strong>Head:</strong>
                            <xsl:call-template name="span">
                                <xsl:with-param name="id" select="$id" />
                            </xsl:call-template>
                        </xsl:for-each>
                        <xsl:for-each select="folia:source">
                            <strong>Source:</strong>
                            <xsl:call-template name="span">
                                <xsl:with-param name="id" select="$id" />
                            </xsl:call-template>
                        </xsl:for-each>
                        <xsl:for-each select="folia:target">
                            <strong>Target:</strong>
                            <xsl:call-template name="span">
                                <xsl:with-param name="id" select="$id" />
                            </xsl:call-template>
                        </xsl:for-each>
                </span><br />
            </xsl:if>
        </xsl:for-each>
    </xsl:for-each>
    </xsl:for-each>
</xsl:template>


<xsl:template match="folia:whitespace">
 <br /><br />
</xsl:template>

<xsl:template match="folia:br">
 <br />
</xsl:template>

<xsl:template match="folia:t-hbr">
<span class="hbr">&#173;</span>
</xsl:template>

<xsl:template match="folia:figure">
 <div class="figure">
  <img>
      <xsl:attribute name="src">
        <xsl:value-of select="@src" />
      </xsl:attribute>
      <xsl:attribute name="alt">
        <xsl:value-of select="folia:desc" />
      </xsl:attribute>
  </img>
  <xsl:if test="folia:caption">
   <div class="caption">
     <xsl:apply-templates />
   </div>
  </xsl:if>
 </div>
</xsl:template>

<xsl:template match="folia:table">
    <table>
      <xsl:apply-templates select="folia:tablehead" />
      <tbody>
        <xsl:apply-templates select="*[name()!='tablehead']" />
      </tbody>
    </table>
</xsl:template>



<xsl:template match="folia:tablehead">
  <thead>
        <xsl:apply-templates />
  </thead>
</xsl:template>


<xsl:template match="folia:row">
  <tr>
        <xsl:apply-templates />
 </tr>
</xsl:template>

<xsl:template match="folia:cell">
  <td>
    <xsl:apply-templates />
  </td>
</xsl:template>


<xsl:template match="folia:su" mode="xml2layout">
 <!-- Enrich SU for conversion to SVG -->

  <xsl:param name="id" />

  <xsl:param name="depth" select="1"/>
  <xsl:variable name="subTree">
    <xsl:copy-of select="folia:wref" />
    <xsl:apply-templates select="folia:su" mode="xml2layout">
      <xsl:with-param name="depth" select="$depth+1"/>
      <xsl:with-param name="id" select="$id"/>
    </xsl:apply-templates>
  </xsl:variable>

  <xsl:variable name="childwidth"><xsl:value-of select="sum(exsl:node-set($subTree)/folia:su/@width)" /></xsl:variable>

  <xsl:variable name="width">
    <xsl:choose>
        <xsl:when test="$childwidth > 1"><xsl:value-of select="$childwidth"/></xsl:when>
        <xsl:otherwise>1</xsl:otherwise>
    </xsl:choose>
  </xsl:variable>

  <!-- Add layout attributes to the existing node -->
  <folia:su depth="{$depth}" width="{$width}">
    <xsl:if test="folia:wref[@id=$id]">
        <xsl:attribute name="selected">selected</xsl:attribute>
    </xsl:if>
    <xsl:copy-of select="@class"/>
    <xsl:copy-of select="$subTree"/>
  </folia:su>

</xsl:template>

<!-- Magnifying factor -->
<xsl:param name="su.scale" select="30"/>

<!-- Convert layout to SVG -->
<xsl:template name="layout2svg">
  <xsl:param name="layout"/>

  <!-- Find depth of the tree -->
  <xsl:variable name="maxDepth">
    <xsl:for-each select="$layout//folia:su">
      <xsl:sort select="@depth" data-type="number" order="descending"/>
      <xsl:if test="position() = 1">
        <xsl:value-of select="@depth"/>
      </xsl:if>
    </xsl:for-each>
  </xsl:variable>

  <xsl:variable name="viewwidth"><xsl:value-of select="sum($layout/folia:su/@width) * 2 * $su.scale" /></xsl:variable>
  <xsl:variable name="viewheight"><xsl:value-of select="$maxDepth * 2 * $su.scale" /></xsl:variable>


   <xsl:choose>
        <xsl:when test="$viewwidth &gt; 1920">(Syntax tree too large to show)</xsl:when>
        <xsl:otherwise>

            <xsl:variable name="rescale">
                <xsl:choose>
                    <xsl:when test="$viewwidth &gt; 1024"><xsl:value-of select="1024 div $viewwidth" /></xsl:when>
                    <xsl:otherwise>1</xsl:otherwise>
                </xsl:choose>
            </xsl:variable>

                <xsl:if test="$viewwidth &gt; 800">(See pop out)</xsl:if>
            <!-- Create SVG wrapper -->
            <svg viewbox="0 0 {$viewwidth}px {$viewheight}px" width="{$viewwidth}" height="{$viewheight + 25}px" preserveAspectRatio="xMidYMid meet">
                <xsl:if test="$viewwidth &gt; 800">
                    <xsl:attribute name="class">bigtree</xsl:attribute>
                </xsl:if>
                <g transform="scale({$rescale})">
                    <rect x="0" y="0" width="{$viewwidth}" height="{$viewheight+25}" style="fill: #b4d4d1;"  />
                    <xsl:apply-templates select="$layout/folia:su" mode="layout2svg"/>
                </g>
            </svg>

    </xsl:otherwise>
  </xsl:choose>

</xsl:template>

<!-- Draw one node -->
<xsl:template match="folia:su" mode="layout2svg">

  <!-- Calculate X coordinate -->
  <xsl:variable name="x" select = "(sum(preceding::folia:su[@depth = current()/@depth or (not(folia:su) and @depth &lt;= current()/@depth)]/@width) + (@width div 2)) * 2"/>
  <!-- Calculate Y coordinate -->
  <xsl:variable name = "y" select = "@depth * 2"/>

  <xsl:variable name="fill">
      <xsl:choose>
          <xsl:when test="@selected">#faffa3</xsl:when>
          <xsl:otherwise>none</xsl:otherwise>
      </xsl:choose>
  </xsl:variable>

  <!-- Draw rounded rectangle around label -->
  <rect x="{($x - 0.9) * $su.scale}" y="{($y - 1) * $su.scale}" width="{1.8 * $su.scale}" height="{1 * $su.scale}" rx="{0.4 * $su.scale}" ry="{0.4 * $su.scale}"
      style = "fill: {$fill}; stroke: black; stroke-width: 1px;"/>

  <!-- Draw label of su -->
  <text x="{$x  * $su.scale}" y="{($y - 0.5) * $su.scale}" style="text-anchor: middle; font-size: 9px; font-weight: normal; fill: #000055;">
    <xsl:value-of select="@class"/>
  </text>
  <text x="{$x  * $su.scale}" y="{($y + 0.3) * $su.scale}" style="text-anchor: middle; font-size: 9px; font-weight: normal;">
    <xsl:for-each select="folia:wref">
        <xsl:choose>
            <xsl:when test="@t">
                <xsl:value-of select="@t" />
                <xsl:text> </xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:if test="//folia:w[@xml:id=$wrefid]">
                    <xsl:value-of select="//folia:w[@xml:id=$wrefid]/folia:t[$ancestors_ok]"/>
                </xsl:if>
                <xsl:text> </xsl:text>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:for-each>
  </text>


  <!-- Draw connector lines to all sub-nodes -->
  <xsl:for-each select="folia:su">
    <line x1 = "{$x*$su.scale}"
              y1 = "{$y*$su.scale}"
              x2 = "{(sum(preceding::folia:su[@depth = current()/@depth or (not(folia:su) and @depth &lt;= current()/@depth)]/@width) + (@width div 2)) * 2 * $su.scale}"
              y2 = "{(@depth * 2 - 1)*$su.scale}"
              style = "stroke-width: 1px; stroke: black;"/>
  </xsl:for-each>
  <!-- Draw sub-nodes -->
  <xsl:apply-templates select="folia:su" mode="layout2svg"/>
</xsl:template>



<xsl:template name="su2svg">
  <xsl:param name="id" />

  <xsl:variable name="tree">
    <xsl:copy-of select="folia:su" />
  </xsl:variable>


  <!-- Add layout information to XML nodes -->
  <xsl:variable name="layoutTree">
    <xsl:apply-templates select="exsl:node-set($tree)/folia:su" mode="xml2layout">
        <xsl:with-param name="id" select="$id" />
    </xsl:apply-templates>
  </xsl:variable>



  <!-- Turn XML nodes into SVG image -->
  <xsl:call-template name="layout2svg">
    <xsl:with-param name="layout" select="exsl:node-set($layoutTree)"/>
    <xsl:with-param name="id" select="$id" />
  </xsl:call-template>

</xsl:template>




</xsl:stylesheet>


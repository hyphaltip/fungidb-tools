#!/usr/bin/env python
"""Template for data source attribution xml.

2012/10/01
Edward Liaw
"""

title =                     ''
pmid =                      ''
display =                   ''
summary =                   ''
protocol =                  ''
description =               ''
url =                       'http://'
contacts = ({'name':        '',
             'email':       '',
             'institution': '',
             'address':     '',
             'city':        '',
             'state':       '',
             'country':     '',
             'zip':         '',
             },
            )
links = (                   '',
         )

CONTACT_ORDER = ('name', 'email', 'institution', 'address', 'city', 'state',
                 'country', 'zip')

CONTACT_HEAD = "       <contact isPrimaryContact=\"{primary}\">"
CONTACT_BODY = "           <{key}>{val}</{key}>"
CONTACT_TAIL = "       </contact>"


def make_contact_block(contacts=contacts):
    """Generate xml section for contacts."""
    contact_block = []
    contact_block.append("    <contacts>")
    primary = 'true'
    for contact in contacts:
        contact_block.append(CONTACT_HEAD.format(primary=primary))
        primary = 'false'
        contact_block.append('\n'.join(CONTACT_BODY.format(
            key=next_field, val=contact[next_field]) for next_field in CONTACT_ORDER))
        contact_block.append(CONTACT_TAIL)
    contact_block.append("    </contacts>")
    return '\n'.join(contact_block)

print("""
  <dataSourceAttribution  resource=\"{title}\" overridingType=\"\" overridingSubtype=\"\" ignore=\"False\">

    <publications>
      <publication pmid=\"{pmid}\"/>
    </publications>

{contact_block}

    <displayName>{display}</displayName>
    <summary><![CDATA[
{summary}
]]>
    </summary>
    <protocol><![CDATA[
{protocol}
]]></protocol>
    <caveat><![CDATA[]]></caveat>
    <acknowledgement><![CDATA[]]></acknowledgement>
    <releasePolicy></releasePolicy>
    <description><![CDATA[
{description}
]]>
    </description>

    <links>
        <link>
           <!-- downloadFile, SupplementaryData, sampleStrategy, publicUrl -->
           <type>publicUrl</type>
           <url>{url}</url>
           <linkDescription></linkDescription>
        </link>
    </links>

    <wdkReference recordClass=\"\" type=\"\" name=\"\"/>

  </dataSourceAttribution>
""".format(title=title, pmid=pmid, display=display,
           contact_block=make_contact_block(contacts), summary=summary,
           protocol=protocol, description=description, url=url))

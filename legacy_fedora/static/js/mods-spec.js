var modsSpec = {
    onchange: function() {
        console.log("I have been changed now");
    },
    elements: {
        "mods:abstract": {
            menu: [{
                caption: "Delete <abstract>",
                action: Xonomy.deleteElement
            }],    
            hasText: true
        },
        "mods:accessCondition": {
            menu: [{
                caption: "Add @type property",
                action: Xonomy.newAttribute,
                actionParameter: { name: "type", value: "" },
                hideIf: function(jsElement) {
                        return jsElement.hasAttribute("type");
                }
            },{
                caption: "Delete <accessCondition>",
                action: Xonomy.deleteElement
            }],
            hasText: true,
            attributes: {
                "type": {
                    asker: Xonomy.askPicklist,
                    askerParameter: [
                        "restriction on access",
                        "use and reproduction"
                    ] 
                }
            }
        },
        "mods:extent": {
            hasText: true,
            menu: [{
                caption: "Delete <extent>",
                action: Xonomy.deleteElement
            }]
        },
        "mods:form": {
            hasText: true,
            menu: [{
                caption: "Delete <form>",
                action: Xonomy.deleteElement
            }],
            attributes: {
                "authority": {
                    asker: Xonomy.askPicklist,
                    askerParameter: [{
                        name: "MARC form of item term list",
                        value: "marcform"
                    }],
                    menu: [{
                        caption: "Delete @authority",
                        action: Xonomy.deleteAttribute
                    }]
                }

            }
        },
        "mods:language": {
            menu: [{
                caption: "Add <languageTerm>",
                action: Xonomy.newElementChild,
                actionParameter: "<mods:languageTerm xmlns:mods='http://www.loc.gov/mods/v3' />"
            },{
                caption: "Delete <language>",
                action: Xonomy.deleteElement                
            }],
            hasText: false
        },
        "mods:languageTerm": {
            menu: [{
                caption: "Delete <languageTerm>",
                action: Xonomy.deleteElement
            }],
            hasText: true
        },
        "mods:mods": {
            menu: [{
                    caption: "Append <abstract>",
                    action: Xonomy.newElementChild,
                    actionParameter: "<mods:abstract xmlns:mods='http://www.loc.gov/mods/v3'/>"
                },
                {
                    caption: "Append <accessCondition>",
                    action: Xonomy.newElementChild,
                    actionParameter: "<mods:accessCondition xmlns:mods='http://www.loc.gov/mods/v3'/>"
                },
                {
                    caption: "Add <classification>",
                    action: Xonomy.newElementChild,
                    actionParameter: "<mods:classification xmlns:mods='http://www.loc.gov/mods/v3'/>"
                },
                {
                    caption: "Add <genre>",
                    action: Xonomy.newElementChild,
                    actionParameter: "<mods:genre xmlns:mods='http://www.loc.gov/mods/v3' />"
                },{
                    caption: "Add <language>",
                    action: Xonomy.newElementChild,
                    actionParameter: "<mods:language xmlns:mods='http://www.loc.gov/mods/v3'><mods:languageTerm /></mods:language>"                
                },{
                    caption: "Add <name>",
                    action: Xonomy.newElementChild,
                    actionParameter: "<mods:name xmlns:mods='http://www.loc.gov/mods/v3'><mods:namePart/><mods:role><mods:roleTerm type=\"text\" authority=\"marcrelator\" /></mods:role></mods:name>"
                },
                {
                    caption: "Add <note>",
                    action: Xonomy.newElementChild,
                    actionParameter: "<mods:note xmlns:mods='http://www.loc.gov/mods/v3'></mods:note>"
                },{
                    caption: "Add <physicalDescription>",
                    action: Xonomy.newElementChild,
                    actionParameter: "<mods:physicalDescription xmlns:mods='http://www.loc.gov/mods/v3'/>"
                },{
                    caption: "Add <subject>",
                    action: Xonomy.newElementChild,
                    actionParameter: "<mods:subject xmlns:mods='http://www.loc.gov/mods/v3' />"
                },
                {
                    caption: "Add <titleInfo>",
                    action: Xonomy.newElementChild,
                    actionParameter: "<mods:titleInfo xmlns:mods='http://www.loc.gov/mods/v3'><mods:title/></mods:titleInfo>"
                },
                {
                    caption: "Add <topic>",
                    action: Xonomy.newElementChild,
                    actionParameter: "<mods:subject xmlns:mods='http://www.loc.gov/mods/v3'><mods:topic /></mods:subject>"
                },
                {
                    caption: "Add <typeOfResource>",
                    action: Xonomy.newElementChild,
                    actionParameter: "<mods:typeOfResource xmlns:mods='http://www.loc.gov/mods/v3' />"
                }
            ],
            hasText: false
        },
        "mods:classification": {
            menu: [{
                caption: "Add @authority attribute",
                action: Xonomy.newAttribute,
                actionParameter: {name: "authority", value: ""}
                }            
            ],
            canDropTo: ["mods"],
            attributes: {
                "authority": {
                    asker: Xonomy.askPicklist,
                    askerParameter: [
                        "codocs",
                        "ddc",
                        "lcc",
                        "sudocs",
                        "z" 
                    ],
                    menu: [{
                        caption: "Delete @authority",
                        action: Xonomy.deleteAttribute
                    }]
                }
            }
        },
        "mods:dateCreated": {
            menu: [{
                caption: "Add @keydate",
                action: Xonomy.newAttribute,
                actionParameter: { name: "keyDate", value: "no"}
            },{
                caption: "Delete <dateCreated>",
                action: Xonomy.deleteElement
            }],
            hasText: true,
            attributes: {
                "keyDate": {
                    asker: Xonomy.askPicklist,
                    askerParameter: [
                        "yes",
                        "no"
                    ]
                }
            }
        },
        "mods:dateIssued": {
            menu: [{
                caption: "Add @keydate",
                action: Xonomy.newAttribute,
                actionParameter: { name: "keyDate", value: "no"}
            },{
                caption: "Delete <dateIssued>",
                action: Xonomy.deleteElement
            }],
            hasText: true,
            attributes: {
                "keyDate": {
                    asker: Xonomy.askPicklist,
                    askerParameter: [
                        "yes",
                        "no"
                    ],
                   menu: [{
                        caption: "Delete @keyDate",
                        action: Xonomy.deleteAttribute
                    }
                    ]
               
                }
            }
        },

        "mods:genre": {
            hasText: true,
            menu: [{
                caption: "Delete <genre>",
                action: Xonomy.deleteElement
            }],
        },
        "mods:identifier": {
            hasText: true,
            menu: [{
                caption: "Add @displayLabel",
                action: Xonomy.newAttribute,
                actionParameter: { name: "displayLabel", value: ""}
            },{
                caption: "Add @type",
                action: Xonomy.newAttribute,
                actionParameter: { name: "type", value: ""}
            },{
                caption: "Delete <identifier>",
                action: Xonomy.deleteElement
            }],
            attributes: {
                 "displayLabel": {
                    asker: Xonomy.askString,
                    menu: [{
                        caption: "Delete @displayLabel",
                        action: Xonomy.deleteAttribute
                    }]
                },
                "type": {
                    asker: Xonomy.askPicklist,
                    askerParameter: [
                        "hdl",
                        "lccn",
                        "local",
                        "isbn",
                        "uri"
                    ],
                }
            }
        },
        "mods:name": {
            menu: [{
                    caption: "Append an <namePart>",
                    action: Xonomy.newElementChild,
                    actionParameter: "<mods:namePart  xmlns:mods='http://www.loc.gov/mods/v3'/>"
                },
                {
                    caption: "Append an <role>",
                    action: Xonomy.newElementChild,
                    actionParameter: "<mods:role xmlns:mods='http://www.loc.gov/mods/v3'><mods:roleTerm /></mods:role>"
                },
                {
                    caption: "Append @type=\"type_of\"",
                    action: Xonomy.newAttribute,
                    actionParameter: {name: "type", value: ""},
                    hideIf: function(jsElement) {
                        return jsElement.hasAttribute("type");
                    }
                },
                {
                    caption: "Add @authorityURI attribute",
                    action: Xonomy.newAttribute,
                    actionParameter: { name: "authorityURI", value: "" }
                },
                {
                    caption: "Add @valueURI attribute",
                    action: Xonomy.newAttribute,
                    actionParameter: { name: "valueURI", value: "" }
                },
                {
                    caption: "Delete <name>",
                    action: Xonomy.deleteElement
                }
            ],
            canDropTo: ["mods", "subject"],
            attributes: {
                "authorityURI": {
                    asker: Xonomy.askString,
                    menu: [{
                        caption: "Delete @authorityURI",
                        action: Xonomy.deleteAttribute
                    }
                    ]
                },
                "type": {
                    asker: Xonomy.askPicklist,
                    askerParameter: [
                        "personal",
                        "corporate",                         
                        "conference",
                        "family"
                    ],
                    menu: [{
                        caption: "Delete @type",
                        action: Xonomy.deleteAttribute
                    }]
                },
                "valueURI": {
                    asker: Xonomy.askString,
                    menu: [{
                        caption: "Delete @authorityURI",
                        action: Xonomy.deleteAttribute
                    }]
                }
            }
        },
        "mods:namePart": {
            menu: [{
                caption: "Delete <namePart>",
                action: Xonomy.deleteElement
            }],
            canDropTo: ["name"],
            hasText: true
        },
        "mods:note": {
           menu: [{ 
                caption: "Add @type=\"{type_of}\"",
                action: Xonomy.newAttribute,
                actionParameter: { name: "type", value: ""},
                hideIf: function(jsElement) {
                    return jsElement.hasAttribute("type");
               }
            },
            {
                caption: "Delete current <note>",
                action: Xonomy.deleteElement
            },
            {
                caption: "New <note>",
                action: Xonomy.newElementAfter,
                actionParameter: "<mods:note xmlns:mods='http://www.loc.gov/mods/v3'></note>"
            }],
           attributes: {
                "displayLabel": {
                    asker: Xonomy.askString,
                    menu: [{
                        caption: "Delete @displayLabel",
                        action: Xonomy.deleteAttribute
                    }]
                },
                "type": {
                    asker: Xonomy.askPicklist,
                    askerParameter: [
                        "admin",
                        "bibliography",
                        "statement of responsibility",
                        "thesis"
                    ],
                    menu: [{
                        caption: "Delete @type",
                        action: Xonomy.deleteAttribute
                    }]

                }
            },
            hasText: true
        },
        "mods:originInfo": {
            menu: [{
                caption: "Add <dateCreated>",
                action: Xonomy.newElementChild,
                actionParameter: "<mods:dateCreated xmlns:mods='http://www.loc.gov/mods/v3'/>"
            },{
                caption: "Add <dateIssued>",
                action: Xonomy.newElementChild,
                actionParameter: "<mods:dateIssued  xmlns:mods='http://www.loc.gov/mods/v3'/>"
            },{
                caption: "Add <publisher>",
                action: Xonomy.newElementChild,
                actionParameter: "<mods:publisher xmlns:mods='http://www.loc.gov/mods/v3'/>"
            },{
                caption: "Add <place>",
                action: Xonomy.newElementChild,
                actionParameter: "<mods:place xmlns:mods='http://www.loc.gov/mods/v3'><mods:placeTerm /></mods:place>"
            },{
                caption: "Delete <originInfo>",
                action: Xonomy.deleteElement
            }]
        },
        "mods:place": {
            menu: [{
                caption: "Add <placeTerm>",
                action: Xonomy.newElementChild,
                actionParameter: "<mods:placeTerm xmlns:mods='http://www.loc.gov/mods/v3' />"
            },
            {
                caption: "Delete <place>",
                action: Xonomy.deleteElement
            }]
        },
        "mods:placeTerm": {
            menu: [{
                caption: "Add @authority property",
                action: Xonomy.newAttribute,
                actionParameter: {name: "authority", value: ""}
            },{
                caption: "Add @type property",
                action: Xonomy.newAttribute,
                actionParameter: {name: "type", value: ""}
            },{
                caption: "Delete <placeTerm>",
                action: Xonomy.deleteElement
            }],
            hasText: true,
            attributes: {
                "authority": {
                   asker: Xonomy.askString,
                   menu: [{
                        caption: "Delete @authority",
                        action: Xonomy.deleteAttribute
                    }]
                 },
                "type": {
                    asker: Xonomy.askPicklist,
                    askerParameter: [
                        "code",
                        "text"
                    ],
                    menu: [{
                        caption: "Delete @type",
                        action: Xonomy.deleteAttribute
                    }]
                }
            }
        },
        "mods:physicalDescription": {
            menu: [{
                caption: "Add <digitalOrigin>",
                action: Xonomy.newElementChild,
                actionParameter: "<mods:digitalOrigin xmlns:mods='http://www.loc.gov/mods/v3' />"
            },{
                caption: "Add <extent>",
                action: Xonomy.newElementChild,
                actionParameter: "<mods:extent xmlns:mods='http://www.loc.gov/mods/v3'/>"
            },{
                caption: "Add <form>",
                action: Xonomy.newElementChild,
                actionParameter: "<mods:form authority=\"marcform\" xmlns:mods='http://www.loc.gov/mods/v3' />"
            },{
                caption: "Delete <physicalDescription>",
                action: Xonomy.deleteElement
            }]
        },
        "mods:publisher": {
            menu: [{
                caption: "Delete <publisher>",
                action: Xonomy.deleteElement
            }],
            hasText: true
        },
        "mods:role": {
            menu: [{
                caption: "Append an <roleTerm>",
                action: Xonomy.newElementChild,
                actionParameter: "<mods:roleTerm/>"
            }]
        },
        "mods:roleTerm": {
            menu: [{
                caption: "Add @type=\"something\"",
                action: Xonomy.newAttribute,
                actionParameter: {name: "type", value: ""}
            }],
            canDropTo: ["role"],
            hasText: true,
            attributes: {
                "type": {
                    asker: Xonomy.askString,
                    menu: [{
                        caption: "Delete @type",
                        action: Xonomy.deleteAttribute
                    }]
                }
            }
        },
        "mods:subject": {
            menu: [{
                caption: "Add @valueURI property",
                action: Xonomy.newAttribute,
                actionParameter: { name: "valueURI", value: ""}
            },
            {
                caption: "Add <topic>",
                action: Xonomy.newElementChild,
                actionParameter: "<mods:topic xmlns:mods='http://www.loc.gov/mods/v3' />"
            },
            {
                caption: "Add <name>",
                action: Xonomy.newElementChild,
                actionParameter: "<mods:name xmlns:mods='http://www.loc.gov/mods/v3'><mods:namePart></mods:namePart></mods:name>"
            },
            {
                caption: "Add <geographic>",
                action: Xonomy.newElementChild,
                actionParameter: "<mods:geographic xmlns:mods='http://www.loc.gov/mods/v3'/>"
            },
            {
                caption: "Add <temporal>",
                action: Xonomy.newElementChild,
                actionParameter: "<mods:temporal xmlns:mods='http://www.loc.gov/mods/v3' />"
            },
            {
                caption: "Add new <subject>",
                action: Xonomy.newElementAfter,
                actionParameter: "<mods:subject xmlns:mods='http://www.loc.gov/mods/v3'/>"
            },
            {
                caption: "Delete <subject>",
                action: Xonomy.deleteElement
            }
            ],
            attributes: {
                "valueURI": {
                    asker: Xonomy.askString,
                    menu: [{
                        caption: "Delete @valueURI",
                        action: Xonomy.deleteAttribute
                    }]
                }
            }

        },
        "mods:subTitle": {
            menu: [{
                caption: "Delete <subTitle>",
                action: Xonomy.deleteElement
            }],
            hasText: true
        },
        "mods:title": {
            menu: [{
                caption: "Delete <title>",
                action: Xonomy.deleteElement
            }],
            hasText: true
        },
       "mods:titleInfo": {
            menu: [{
                caption: "Add a <title>",
                action: Xonomy.newElementChild,
                actionParameter: "<mods:title xmlns:mods='http://www.loc.gov/mods/v3'/>"
            },{
                caption: "Add a <subTitle>",
                action: Xonomy.newElementChild,
                actionParameter: "<mods:subTitle xmlns:mods='http://www.loc.gov/mods/v3'/>"
            },{
                caption: "Delete <titleInfo>",
                action: Xonomy.deleteElement
            }],
        },
        "mods:topic": {
            menu: [{
                caption: "Delete <topic>",
                action: Xonomy.deleteElement
            }],
            hasText: true
        },
        "mods:typeOfResource": {
            menu: [{
                caption: "Delete <typeOfResource>",
                action: Xonomy.deleteElement
            }],
            hasText: true,
            asker: Xonomy.askPicklist,
            askerParameter: [
                "text",
                "cartographic",
                "notated music",
                "sound recording",
                "sound recording-musical",
                "sound recording-nonmusical",
                "still image",
                "moving image",
                "three dimensional object",
                "software, multimedia",
                "mixed material" 
            ]
        }
    }
};

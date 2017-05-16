var modsSpec = {
    onchange: function() {
        console.log("I have been changed now");
    },
    elements: {
        "abstract": {
            menu: [{
                caption: "Delete <abstract>",
                action: Xonomy.deleteElement
            }],    
            hasText: true
        },
        "accessCondition": {
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
        "extent": {
            hasText: true,
            menu: [{
                caption: "Delete <extent>",
                action: Xonomy.deleteElement
            }]
        },
        "form": {
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
        "language": {
            menu: [{
                caption: "Add <languageTerm>",
                action: Xonomy.newElementChild,
                actionParameter: "<languageTerm />"
            },{
                caption: "Delete <language>",
                action: Xonomy.deleteElement                
            }],
            hasText: false
        },
        "languageTerm": {
            menu: [{
                caption: "Delete <languageTerm>",
                action: Xonomy.deleteElement
            }],
            hasText: true
        },
        "mods": {
            menu: [{
                    caption: "Append <abstract>",
                    action: Xonomy.newElementChild,
                    actionParameter: "<abstract/>"
                },
                {
                    caption: "Append <accessCondition>",
                    action: Xonomy.newElementChild,
                    actionParameter: "<accessCondition/>"
                },
                {
                    caption: "Add <classification>",
                    action: Xonomy.newElementChild,
                    actionParameter: "<classification/>"
                },
                {
                    caption: "Add <genre>",
                    action: Xonomy.newElementChild,
                    actionParameter: "<genre/>"
                },{
                    caption: "Add <language>",
                    action: Xonomy.newElementChild,
                    actionParameter: "<language><languageTerm /></language>"                
                },{
                    caption: "Add <name>",
                    action: Xonomy.newElementChild,
                    actionParameter: "<name><namePart/><role><roleTerm type=\"text\" authority=\"marcrelator\" /></role></name>"
                },
                {
                    caption: "Add <note>",
                    action: Xonomy.newElementChild,
                    actionParameter: "<note></note>"
                },{
                    caption: "Add <physicalDescription>",
                    action: Xonomy.newElementChild,
                    actionParameter: "<physicalDescription/>"
                },{
                    caption: "Add <subject>",
                    action: Xonomy.newElementChild,
                    actionParameter: "<subject />"
                },
                {
                    caption: "Add <titleInfo>",
                    action: Xonomy.newElementChild,
                    actionParameter: "<titleInfo><title/></titleInfo>"
                },
                {
                    caption: "Add <topic>",
                    action: Xonomy.newElementChild,
                    actionParameter: "<subject><topic /></subject>"
                }

            ],
            hasText: false
        },
        "classification": {
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
        "dateCreated": {
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
        "dateIssued": {
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

        "genre": {
            hasText: true,
            menu: [{
                caption: "Delete <genre>",
                action: Xonomy.deleteElement
            }],
        },
        "identifier": {
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
        "name": {
            menu: [{
                    caption: "Append an <namePart>",
                    action: Xonomy.newElementChild,
                    actionParameter: "<namePart />"
                },
                {
                    caption: "Append an <role>",
                    action: Xonomy.newElementChild,
                    actionParameter: "<role><roleTerm /></role>"
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
        "namePart": {
            menu: [{
                caption: "Delete <namePart>",
                action: Xonomy.deleteElement
            }],
            canDropTo: ["name"],
            hasText: true
        },
        "note": {
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
                actionParameter: "<note></note>"
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
        "originInfo": {
            menu: [{
                caption: "Add <dateCreated>",
                action: Xonomy.newElementChild,
                actionParameter: "<dateCreated/>"
            },{
                caption: "Add <dateIssued>",
                action: Xonomy.newElementChild,
                actionParameter: "<dateIssued />"
            },{
                caption: "Add <publisher>",
                action: Xonomy.newElementChild,
                actionParameter: "<publisher />"
            },{
                caption: "Add <place>",
                action: Xonomy.newElementChild,
                actionParameter: "<place><placeTerm /></place>"
            },{
                caption: "Delete <originInfo>",
                action: Xonomy.deleteElement
            }]
        },
        "place": {
            menu: [{
                caption: "Add <placeTerm>",
                action: Xonomy.newElementChild,
                actionParameter: "<placeTerm/>"
            },
            {
                caption: "Delete <place>",
                action: Xonomy.deleteElement
            }]
        },
        "placeTerm": {
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
        "physicalDescription": {
            menu: [{
                caption: "Add <digitalOrigin>",
                action: Xonomy.newElementChild,
                actionParameter: "<digitalOrigin />"
            },{
                caption: "Add <extent>",
                action: Xonomy.newElementChild,
                actionParameter: "<extent />"
            },{
                caption: "Add <form>",
                action: Xonomy.newElementChild,
                actionParameter: "<form authority=\"marcform\"/>"
            },{
                caption: "Delete <physicalDescription>",
                action: Xonomy.deleteElement
            }]
        },
        "publisher": {
            menu: [{
                caption: "Delete <publisher>",
                action: Xonomy.deleteElement
            }],
            hasText: true
        },
        "role": {
            menu: [{
                caption: "Append an <roleTerm>",
                action: Xonomy.newElementChild,
                actionParameter: "<roleTerm/>"
            }]
        },
        "roleTerm": {
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
        "subject": {
            menu: [{
                caption: "Add @valueURI property",
                action: Xonomy.newAttribute,
                actionParameter: { name: "valueURI", value: ""}
            },
            {
                caption: "Add <topic>",
                action: Xonomy.newElementChild,
                actionParameter: "<topic/>"
            },
            {
                caption: "Add <name>",
                action: Xonomy.newElementChild,
                actionParameter: "<name><namePart></namePart></name>"
            },
            {
                caption: "Add <geographic>",
                action: Xonomy.newElementChild,
                actionParameter: "<geographic />"
            },
            {
                caption: "Add <temporal>",
                action: Xonomy.newElementChild,
                actionParameter: "<temporal />"
            },
            {
                caption: "Add new <subject>",
                action: Xonomy.newElementAfter,
                actionParameter: "<subject />"
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
        "subTitle": {
            menu: [{
                caption: "Delete <subTitle>",
                action: Xonomy.deleteElement
            }],
            hasText: true
        },
        "title": {
            menu: [{
                caption: "Delete <title>",
                action: Xonomy.deleteElement
            }],
            hasText: true
        },
       "titleInfo": {
            menu: [{
                caption: "Add a <title>",
                action: Xonomy.newElementChild,
                actionParameter: "<title/>"
            },{
                caption: "Add a <subTitle>",
                action: Xonomy.newElementChild,
                actionParameter: "<subTitle/>"
            },{
                caption: "Delete <titleInfo>",
                action: Xonomy.deleteElement
            }]
        },
        "topic": {
            menu: [{
                caption: "Delete <topic>",
                action: Xonomy.deleteElement
            }],
            hasText: true
        }
    }
};

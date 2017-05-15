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
                    actionParameter: "<name><namePart/><role><roleTerm type=\"text\" authorit=\"marcrelator\" /></role></name>"
                },
                {
                    caption: "Add <note>",
                    action: Xonomy.newElementChild,
                    actionParameter: "<note></note>"
                },
                {
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
        "genre": {
            hasText: true,
            menu: [{
                caption: "Delete <genre>",
                action: Xonomy.deleteElement
            }],
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
                caption: "Delete <placeTerm>",
                action: Xonomy.deleteElement
            }],
            hasText: true
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

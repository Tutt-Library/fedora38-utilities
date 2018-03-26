"""Elasticsearch Mapping for DACC Repository"""
__author__ = "Jeremy Nelson"

MAP = {"mappings": {
    "mods": {
        "properties": {
            "abstract": {
                "type": "text"
            },
            "adminNote": {
                "type": "text"
            },
            "content_models": {
              # "index": "false",
                       "type": "text"
            },
            "contributor": {
                "type": "text"
            },
            "creator": {
                "type": "text"
            },
            "datastreams": {
               "properties": {
                       "dsid": {
                           # "index": "false",
                           "type": "text"
                       },
					   "label": {
                           # "index": "false",
                           "type": "text"
                       },
                       "mimeType": {
                           # "index": "false",
                           "type": "text"
                       }
                }
            },
            "dateCreated": {
               # "index": "false",
                "type": "text"
            },
            "dateIssued": {
                "type": "text"
            },
            "datePublished": {
                # "index": "false",
                "type": "text"
	    },
            "degreeGrantor": {
                "type": "text"
            },
            "degreeName": {
                "type": "text"
            },
            "degreeType": {
                "type": "text"
            },
            "digitalOrigin": {
                "type": "text"
            },
            "extent": {
                "type": "text"
            },
            "genre": {
             #   # "index": "false",
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }
            },
            "handle": {
                "type": "text"
            },
            "inCollections": {
                "type": "keyword"
            },
            "language": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type":"keyword"
                    }
                }
            },
            "note": {
                "type": "text"
            },
            "parent": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }
            },
            "photographer": {
                "type": "text"
            },

            "pid": {
               # # "index": "false",
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }
            },
            "place": {
                "type": "text"
            },
            "publisher": {
                "type": "text"
            },
            "publicationYear": {             
             #   # "index": "false",
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }
            },
            "sponsor": {
                "type": "text"
            },
            "subject": {
                "properties": {
                    "genre": {
			# "index": "false",
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "geographic": {
		        # "index": "false",
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }

                    },
                    "temporal": {
		        # "index": "false",
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }

                    },
                    "topic": {
			# "index": "false",
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    }
                }
            },
            "thesis": {
                "type": "text"
            },
            "thesisAdvisor": {
                "type": "text"
            },
            "titleAlternative": {
                "type": "text"
            },
            "titlePrincipal": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }

            },
            "titleRaw": {
                "type": "text",
                "index": "false"
            },
            "typeOfResource": {
                # "index": "false",
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }
            },
            "useAndReproduction": {
                "type": "text"
            }
            }
        }
    }
}

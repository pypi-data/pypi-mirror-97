#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Nmap Samples."""
import inspect

add = dict({field: {
    "finished": {
        "time": "1611665445", "timestr": "Tue Jan 26 12:50:45 2021",
        "summary": "Nmap done at Tue Jan 26 12:50:45 2021; 1 IP address (1 host up) scanned in 394.81 seconds",
        "elapsed": "394.81", "exit": "success"
    }, "hosts": {"up": "1", "down": "0", "total": "1"}
} if field == 'runstats' else str() for field in
            ["runstats", "scaninfo", "scanner", "start", "startstr", "verbose", "version",
             "xmloutputversion"]})
samples = {
    # tcp
    '94.130.131.107': dict(
        host={
            "starttime": "1611663986",
            "endtime": "1611664445",
            "status": {"state": "up", "reason": "user-set", "reason_ttl": "0"},
            "address": {"addr": "94.130.131.107", "addrtype": "ipv4"},
            "hostnames": {"hostname": {"name": "static.107.131.130.94.clients.your-server.de", "type": "PTR"}},
            "ports": {
                "extraports": [{
                    "state": "open|filtered", "count": "131070",
                    "extrareasons": {"reason": "no-responses", "count": "131070"}
                }, {
                    "state": "filtered", "count": "65533",
                    "extrareasons": {"reason": "no-responses", "count": "65533"}
                }],
                "port": [{
                    "protocol": "tcp", "portid": "80",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "44"},
                    "service": {"name": "http", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "443",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "44"},
                    "service": {"name": "https", "method": "table", "conf": "3"}
                }]
            }, "times": {"srtt": "86246", "rttvar": "134", "to": "100000"}
        },
    ) | add,
    '136.243.155.166': dict(
        host={
            "starttime": "1611733247", "endtime": "1611759487",
            "status": {"state": "up", "reason": "user-set", "reason_ttl": "0"},
            "address": {"addr": "136.243.155.166", "addrtype": "ipv4"},
            "hostnames": {"hostname": {"name": "static.166.155.243.136.clients.your-server.de", "type": "PTR"}},
            "ports": {
                "extraports": [{
                    "state": "open|filtered", "count": "131070",
                    "extrareasons": {"reason": "no-responses", "count": "131070"}
                }, {
                    "state": "filtered", "count": "65535",
                    "extrareasons": {"reason": "no-responses", "count": "65535"}
                }]
            }
        },
    ) | add,
    '88.99.27.146': dict(
        host={
            "starttime": "1611662482", "endtime": "1611732374",
            "status": {"state": "up", "reason": "user-set", "reason_ttl": "0"},
            "address": {"addr": "88.99.27.146", "addrtype": "ipv4"},
            "hostnames": {"hostname": {"name": "static.146.27.99.88.clients.your-server.de", "type": "PTR"}},
            "ports": {
                "extraports": [{
                    "state": "closed", "count": "131015",
                    "extrareasons": [{"reason": "resets", "count": "65532"},
                                     {"reason": "port-unreaches", "count": "65483"}]
                }, {
                    "state": "open|filtered", "count": "65295",
                    "extrareasons": {"reason": "no-responses", "count": "65295"}
                }, {
                    "state": "filtered", "count": "293",
                    "extrareasons": [{"reason": "proto-unreaches", "count": "292"},
                                     {"reason": "no-response", "count": "1"}]
                }],
                "port": [{
                    "protocol": "tcp", "portid": "22",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "44"},
                    "service": {"name": "ssh", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "222",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "44"},
                    "service": {"name": "rsh-spx", "method": "table", "conf": "3"}
                }]
            }, "times": {"srtt": "86406", "rttvar": "132", "to": "100000"}
        },
    ) | add,
    '88.99.100.233': dict(
        host={
            "starttime": "1611733255", "endtime": "1611759495",
            "status": {"state": "up", "reason": "user-set", "reason_ttl": "0"},
            "address": {"addr": "88.99.100.233", "addrtype": "ipv4"},
            "hostnames": {"hostname": {"name": "static.88-99-100-233.clients.your-server.de", "type": "PTR"}},
            "ports": {
                "extraports": [{
                    "state": "open|filtered", "count": "131070",
                    "extrareasons": {"reason": "no-responses", "count": "131070"}
                }, {
                    "state": "filtered", "count": "65535",
                    "extrareasons": {"reason": "no-responses", "count": "65535"}
                }],
                "port": [{
                    "protocol": "tcp", "portid": "22",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "44"},
                    "service": {
                        "name": "ssh", "product": "OpenSSH", "version": "7.6p1 Ubuntu 4ubuntu0.3",
                        "extrainfo": "Ubuntu Linux; protocol 2.0", "ostype": "Linux", "method": "probed",
                        "conf": "10",
                        "cpe": ["cpe:/a:openbsd:openssh:7.6p1", "cpe:/o:linux:linux_kernel"]
                    }, "script": {
                        "id": "ssh-hostkey",
                        "output": "\n  2048 ad:83:6c:ef:e4:45:f6:0f:d3:5e:a6:4f:f2:f8:0c:c2 (RSA)\n  256 "
                                  "09:cb:2e:c5:d4:4b:59:0f:50:48:b5:95:c8:1a:7d:ec (ECDSA)\n  256 "
                                  "92:b9:e9:82:fb:26:bc:c2:bf:72:00:9b:ca:81:12:87 (ED25519)",
                        "table": [{
                            "elem": [{"key": "fingerprint", "#text": "ad836cefe445f60fd35ea64ff2f80cc2"}, {
                                "key": "key",
                                "#text":
                                    "AAAAB3NzaC1yc2EAAAADAQABAAABAQDi+R34Gn4cV2ZxTwl6TQNhs73kvgz8Ehqk6Iklbf2ka8RbLQgE6G/7WJtuErXvMI+4w1rMC+N75K1MxZPdrTpzfp1VsffjzpKfiPC/7hOLEUzVcFZhCEL4xJGgMtbAT1AFvXdp1bJkfIIEw27yY1VaoQEXkwrawomrMN8AU/Pz1PRwiwAf6fwVy1YkVOx3nliPryfytCVOu4E1mhubk/kVvE5u6swaZYOS73LSnh6JbJyELyw8sWz2DfjjefhMxgEJXFhNv4Bxi8eUKH2K4fgJuLqCLNaF2NHC/uhOBOQqxYrpEPQtaj0NIrQc9gKK7gJKhdGASYqo0fj/Eu0rH7//"
                            }, {"key": "type", "#text": "ssh-rsa"}, {"key": "bits", "#text": "2048"}]
                        }, {
                            "elem": [{"key": "fingerprint", "#text": "09cb2ec5d44b590f5048b595c81a7dec"}, {
                                "key": "key",
                                "#text":
                                    "AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBMPTr17Sc04GUvoqWSWl9o8q2Ai8lBq90zeOdHr+RUqjzla0toLbEPQJn95a0neak6lDNKzU1+uYy/p3L5m8M6Q="
                            }, {"key": "type", "#text": "ecdsa-sha2-nistp256"}, {"key": "bits", "#text": "256"}]
                        }, {
                            "elem": [{"key": "fingerprint", "#text": "92b9e982fb26bcc2bf72009bca811287"}, {
                                "key": "key",
                                "#text": "AAAAC3NzaC1lZDI1NTE5AAAAIBb0GVbfw63D+wZWTffhRQupEX3/1ArFj66DsdZ3giFZ"
                            }, {"key": "type", "#text": "ssh-ed25519"}, {"key": "bits", "#text": "256"}]
                        }]
                    }
                }, {
                    "protocol": "tcp", "portid": "80",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "44"}, "service": {
                        "name": "http", "product": "nginx", "version": "1.14.0", "extrainfo": "Ubuntu",
                        "ostype": "Linux",
                        "method": "probed", "conf": "10",
                        "cpe": ["cpe:/a:igor_sysoev:nginx:1.14.0", "cpe:/o:linux:linux_kernel"]
                    }
                }, {
                    "protocol": "tcp", "portid": "443",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "44"},
                    "service": {
                        "name": "http", "product": "nginx", "version": "1.14.0", "extrainfo": "Ubuntu",
                        "ostype": "Linux",
                        "tunnel": "ssl", "method": "probed", "conf": "10",
                        "cpe": ["cpe:/a:igor_sysoev:nginx:1.14.0", "cpe:/o:linux:linux_kernel"]
                    },
                    "script": [
                        {
                            "id": "http-server-header", "output": "nginx/1.14.0 (Ubuntu)",
                            "elem": "nginx/1.14.0 (Ubuntu)"
                        }, {
                            "id": "http-title", "output": "CodiMD - Collaborative markdown notes",
                            "elem": {"key": "title", "#text": "CodiMD - Collaborative markdown notes"}
                        }, {
                            "id": "ssl-cert",
                            "output": "Subject: commonName=hackmd.nference.net\nSubject Alternative Name: "
                                      "DNS:hackmd.nference.net\nNot valid before: 2020-09-21T23:49:42\nNot valid "
                                      "after:  "
                                      "2020-12-20T23:49:42",
                            "table": [
                                {"key": "subject", "elem": {"key": "commonName", "#text": "hackmd.nference.net"}}, {
                                    "key": "issuer",
                                    "elem": [{"key": "commonName", "#text": "Let's Encrypt Authority X3"},
                                             {"key": "countryName", "#text": "US"},
                                             {"key": "organizationName", "#text": "Let's Encrypt"}]
                                }, {
                                    "key": "pubkey",
                                    "elem": [{"key": "bits", "#text": "2048"}, {"key": "type", "#text": "rsa"},
                                             {"key": "exponent", "#text": "userdata: 0x55623606d718"},
                                             {"key": "modulus", "#text": "userdata: 0x55623606d758"}]
                                }, {
                                    "key": "extensions", "table": [{
                                        "elem": [{"key": "critical", "#text": "true"},
                                                 {
                                                     "key": "name",
                                                     "#text": "X509v3 Key Usage"
                                                 }, {
                                                     "key": "value",
                                                     "#text": "Digital Signature, "
                                                              "Key Encipherment"
                                                 }]
                                    }, {
                                        "elem": [{
                                            "key": "value",
                                            "#text": "TLS Web Server "
                                                     "Authentication, "
                                                     "TLS Web Client "
                                                     "Authentication"
                                        }, {
                                            "key": "name",
                                            "#text": "X509v3 Extended Key "
                                                     "Usage"
                                        }]
                                    }, {
                                        "elem": [{"key": "critical", "#text": "true"},
                                                 {
                                                     "key": "name",
                                                     "#text": "X509v3 Basic "
                                                              "Constraints"
                                                 },
                                                 {"key": "value", "#text": "CA:FALSE"}]
                                    }, {
                                        "elem": [{
                                            "key": "value",
                                            "#text":
                                                "20:1E:54:F7:9C:80:47:0C:05:64:27:C9:17:3C:58:0D:5A:56:F2:46"
                                        }, {
                                            "key": "name",
                                            "#text": "X509v3 Subject Key "
                                                     "Identifier"
                                        }]
                                    }, {
                                        "elem": [{
                                            "key": "value",
                                            "#text":
                                                "keyid:A8:4A:6A:63:04:7D:DD:BA:E6:D1:39:B7:A6:45:65:EF:F3:A8:EC:A1"
                                        }, {
                                            "key": "name",
                                            "#text": "X509v3 Authority Key "
                                                     "Identifier"
                                        }]
                                    }, {
                                        "elem": [{
                                            "key": "value",
                                            "#text": "OCSP - "
                                                     "URI:http://ocsp.int-x3.letsencrypt.org\nCA Issuers - "
                                                     "URI:http://cert.int-x3.letsencrypt.org/"
                                        }, {
                                            "key": "name",
                                            "#text": "Authority Information"
                                                     " Access"
                                        }]
                                    }, {
                                        "elem": [{
                                            "key": "value",
                                            "#text": "DNS:hackmd.nference.net"
                                        }, {
                                            "key": "name",
                                            "#text": "X509v3 Subject "
                                                     "Alternative Name"
                                        }]
                                    }, {
                                        "elem": [{
                                            "key": "value",
                                            "#text": "Policy: 2.23.140.1.2.1\nPolicy: 1.3.6.1.4.1.44947.1.1.1\n  "
                                                     "CPS: http://cps.letsencrypt.org"
                                        }, {
                                            "key": "name",
                                            "#text": "X509v3 Certificate Policies"
                                        }]
                                    }, {
                                        "elem": [{
                                            "key": "value",
                                            "#text": "Signed Certificate Timestamp:\n    Version   : v1 (0x0)\n   "
                                                     " Log ID    : "
                                                     "5E:A7:73:F9:DF:56:C0:E7:B5:36:48:7D:D0:49:E0:32:\n          "
                                                     "      7A:91:9A:0C:84:A1:12:12:84:18:75:96:81:71:45:58\n    "
                                                     "Timestamp : Sep 22 00:49:42.425 2020 GMT\n    Extensions: "
                                                     "none\n    Signature : ecdsa-with-SHA256\n                "
                                                     "30:46:02:21:00:BD:A7:7E:05:99:00:3E:45:39:EE:05:\n          "
                                                     "      FF:B9:0A:6C:A5:75:BE:3E:26:DE:86:74:9B:FF:4C:68:\n    "
                                                     "            "
                                                     "0A:78:97:99:EA:02:21:00:8B:47:B9:74:21:21:D5:DE:\n          "
                                                     "      65:76:E9:28:5D:1E:C6:CE:F7:B5:9A:1B:19:6A:24:96:\n    "
                                                     "            97:81:F4:58:60:F3:EE:95\nSigned Certificate "
                                                     "Timestamp:\n    Version   : v1 (0x0)\n    Log ID    : "
                                                     "07:B7:5C:1B:E5:7D:68:FF:F1:B0:C6:1D:23:15:C7:BA:\n          "
                                                     "      E6:57:7C:57:94:B7:6A:EE:BC:61:3A:1A:69:D3:A2:1C\n    "
                                                     "Timestamp : Sep 22 00:49:42.457 2020 GMT\n    Extensions: "
                                                     "none\n    Signature : ecdsa-with-SHA256\n                "
                                                     "30:45:02:21:00:B7:2D:AA:58:27:33:C1:F0:BD:BB:33:\n          "
                                                     "      98:44:C7:88:83:D4:28:A7:E4:AD:9D:2B:38:12:54:FE:\n    "
                                                     "            "
                                                     "37:B3:22:4C:73:02:20:17:8E:7E:F8:39:73:8C:7B:2C:\n          "
                                                     "      7B:0D:07:72:32:90:F3:25:93:4A:B6:EA:4E:43:06:47:\n    "
                                                     "            FF:E2:74:B6:59:80:0A"
                                        }, {
                                            "key": "name",
                                            "#text": "CT Precertificate SCTs"
                                        }]
                                    }]
                                }, {
                                    "key": "validity", "elem": [{"key": "notAfter", "#text": "2020-12-20T23:49:42"},
                                                                {
                                                                    "key": "notBefore",
                                                                    "#text": "2020-09-21T23:49:42"
                                                                }]
                                }], "elem": [{"key": "sig_algo", "#text": "sha256WithRSAEncryption"},
                                             {"key": "md5", "#text": "5f6a165576ca75fb6bdc79e2b7689bbf"},
                                             {"key": "sha1", "#text": "9337e8940a5e73c63e4799803b9da0021e740961"}, {
                                                 "key": "pem",
                                                 "#text": "-----BEGIN "
                                                          "CERTIFICATE-----\nMIIFXzCCBEegAwIBAgISBOtU1CwFcYuMBzffPMNezXQ/MA0GCSqGSIb3DQEBCwUA\nMEoxCzAJBgNVBAYTAlVTMRYwFAYDVQQKEw1MZXQncyBFbmNyeXB0MSMwIQYDVQQD\nExpMZXQncyBFbmNyeXB0IEF1dGhvcml0eSBYMzAeFw0yMDA5MjEyMzQ5NDJaFw0y\nMDEyMjAyMzQ5NDJaMB4xHDAaBgNVBAMTE2hhY2ttZC5uZmVyZW5jZS5uZXQwggEi\nMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCvbd7sMMUZeNRMjQldDeth5Q0a\nAOtTSBwRVozVPOm+aTlf6MgdrHWDJZ6k5tCa9VO7kcVjUt1QN3iQA+lROVxM6yRb\nw/4v7iwhxqRKGB5jb0SqATWjZgc/ga56v2jyx4gIImraSRnWLaPFtOoqQijnIGSY\nOuch4Q+CEmu+Pi+NBhiT632skaYmsXE/Ywr/sYwR+wSaD5E3cvA+1Wr76kX8MSHF\nxTYttGtLdIx/78srlJsLNYvuOVvBrPQT+NXhwJKqqnqReS5eaLLCLRpjr+KQlSwf\niutRjE4lUVjzKPUyL4WvVusBVp9duiokL/nTa1FNQ9ctPAOwdZCm/79OMGldAgMB\nAAGjggJpMIICZTAOBgNVHQ8BAf8EBAMCBaAwHQYDVR0lBBYwFAYIKwYBBQUHAwEG\nCCsGAQUFBwMCMAwGA1UdEwEB/wQCMAAwHQYDVR0OBBYEFCAeVPecgEcMBWQnyRc8\nWA1aVvJGMB8GA1UdIwQYMBaAFKhKamMEfd265tE5t6ZFZe/zqOyhMG8GCCsGAQUF\nBwEBBGMwYTAuBggrBgEFBQcwAYYiaHR0cDovL29jc3AuaW50LXgzLmxldHNlbmNy\neXB0Lm9yZzAvBggrBgEFBQcwAoYjaHR0cDovL2NlcnQuaW50LXgzLmxldHNlbmNy\neXB0Lm9yZy8wHgYDVR0RBBcwFYITaGFja21kLm5mZXJlbmNlLm5ldDBMBgNVHSAE\nRTBDMAgGBmeBDAECATA3BgsrBgEEAYLfEwEBATAoMCYGCCsGAQUFBwIBFhpodHRw\nOi8vY3BzLmxldHNlbmNyeXB0Lm9yZzCCAQUGCisGAQQB1nkCBAIEgfYEgfMA8QB3\nAF6nc/nfVsDntTZIfdBJ4DJ6kZoMhKESEoQYdZaBcUVYAAABdLNJphkAAAQDAEgw\nRgIhAL2nfgWZAD5FOe4F/7kKbKV1vj4m3oZ0m/9MaAp4l5nqAiEAi0e5dCEh1d5l\ndukoXR7Gzve1mhsZaiSWl4H0WGDz7pUAdgAHt1wb5X1o//Gwxh0jFce65ld8V5S3\nau68YToaadOiHAAAAXSzSaY5AAAEAwBHMEUCIQC3LapYJzPB8L27M5hEx4iD1Cin\n5K2dKzgSVP43syJMcwIgF45++DlzjHssew0HcjKQ8yWTSrbqTkMGR//idLZZgAow\nDQYJKoZIhvcNAQELBQADggEBADRB52sp52hkGox5DGhOZhTFvm2CPNhoW9JziNwm\nhmxzGxhLxqDKFrd9tY1U2g6YQKk1BxY1v/9qMa3YLeDlCn2hVu1fHZr8Ggootvbq\nhPXqFELkorvSBNEBqUewbhTEbmCsnB+6Eg6kzn9PWur7mMkzrrT2mWcnKr3TCh0L\nFsEhWpEAb/WGZKJ2rDcdIslNSYlOSCpVkPEAB+NI19E0Q5/quP740hfH2r2U33A4\njHT/E1APRYsh15iOJq7QCceUpFjaurTVKL0sEANxmNajFX6z9O3WSvihF1EaQLC4\nXXVbomohyqiLsXOqYWNZqW/zQgPbtmlSWGhjgoZ3JQfYC5E=\n-----END CERTIFICATE-----"
                                             }]
                        }, {"id": "tls-alpn", "output": "\n  h2\n  http/1.1", "elem": ["h2", "http/1.1"]},
                        {"id": "tls-nextprotoneg", "output": "\n  h2\n  http/1.1", "elem": ["h2", "http/1.1"]}]
                }, {
                    "protocol": "tcp", "portid": "3000",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "43"},
                    "service": {
                        "name": "http", "product": "Node.js Express framework", "method": "probed", "conf": "10",
                        "cpe": "cpe:/a:nodejs:node.js"
                    }
                }]
            }
        },
    ) | add,
    '54.39.18.19': dict(
        host={
            "starttime": "1611662528", "endtime": "1611732261",
            "status": {"state": "up", "reason": "user-set", "reason_ttl": "0"},
            "address": {"addr": "54.39.18.19", "addrtype": "ipv4"},
            "hostnames": {"hostname": {"name": "ns556065.ip-54-39-18.net", "type": "PTR"}}, "ports": {
                "extraports": [{
                    "state": "closed", "count": "131011",
                    "extrareasons": [{"reason": "resets", "count": "65530"},
                                     {"reason": "port-unreaches", "count": "65481"}]
                }, {
                    "state": "open|filtered", "count": "65320",
                    "extrareasons": {"reason": "no-responses", "count": "65320"}
                }, {
                    "state": "filtered", "count": "270",
                    "extrareasons": [{"reason": "proto-unreaches", "count": "269"},
                                     {"reason": "no-response", "count": "1"}]
                }],
                "port": [{
                    "protocol": "tcp", "portid": "22",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {"name": "ssh", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "111",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {"name": "rpcbind", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "3128",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {"name": "squid-http", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "8006",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {"name": "wpl-analytics", "method": "table", "conf": "3"}
                }]
            }, "times": {"srtt": "15860", "rttvar": "2261", "to": "100000"}
        },
    ) | add,
    '135.181.36.57': dict(
        host={
            "starttime": "1611734581", "endtime": "1611735176",
            "status": {"state": "up", "reason": "user-set", "reason_ttl": "0"},
            "address": {"addr": "135.181.36.57", "addrtype": "ipv4"},
            "hostnames": {"hostname": {"name": "static.57.36.181.135.clients.your-server.de", "type": "PTR"}},
            "ports": {
                "extraports": [{
                    "state": "open|filtered", "count": "131067",
                    "extrareasons": {"reason": "no-responses", "count": "131067"}
                }, {
                    "state": "filtered", "count": "65532",
                    "extrareasons": {"reason": "no-responses", "count": "65532"}
                }],
                "port": [{
                    "protocol": "tcp", "portid": "22",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "27"},
                    "service": {"name": "ssh", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "80",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "27"},
                    "service": {"name": "http", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "443",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "24"},
                    "service": {"name": "https", "method": "table", "conf": "3"}
                }, {
                    "protocol": "udp", "portid": "22", "state": {
                        "state": "closed", "reason": "port-unreach", "reason_ttl": "27"
                    }, "service": {"name": "ssh", "method": "table", "conf": "3"}
                }, {
                    "protocol": "udp", "portid": "80", "state": {
                        "state": "closed", "reason": "port-unreach", "reason_ttl": "27"
                    }, "service": {"name": "http", "method": "table", "conf": "3"}
                }, {
                    "protocol": "udp", "portid": "443", "state": {
                        "state": "closed", "reason": "port-unreach", "reason_ttl": "27"
                    }, "service": {"name": "https", "method": "table", "conf": "3"}
                }]
            }, "times": {"srtt": "102370", "rttvar": "1235", "to": "107310"}
        },
    ) | add,
    '195.201.80.223': dict(
        host={
            "starttime": "1611778194", "endtime": "1611781327",
            "status": {"state": "up", "reason": "user-set", "reason_ttl": "0"},
            "address": {"addr": "195.201.80.223", "addrtype": "ipv4"},
            "hostnames": {"hostname": {"name": "static.223.80.201.195.clients.your-server.de", "type": "PTR"}},
            "ports": {
                "extraports": [{
                    "state": "open|filtered", "count": "131065",
                    "extrareasons": {"reason": "no-responses", "count": "131065"}
                }, {
                    "state": "filtered", "count": "65530",
                    "extrareasons": {"reason": "no-responses", "count": "65530"}
                }],
                "port": [{
                    "protocol": "tcp", "portid": "4445",
                    "state": {"state": "closed", "reason": "reset", "reason_ttl": "44"},
                    "service": {"name": "upnotifyp", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "8700",
                    "state": {"state": "closed", "reason": "reset", "reason_ttl": "44"}
                }, {
                    "protocol": "tcp", "portid": "8796",
                    "state": {"state": "closed", "reason": "reset", "reason_ttl": "44"}
                }, {
                    "protocol": "tcp", "portid": "8798",
                    "state": {"state": "closed", "reason": "reset", "reason_ttl": "44"},
                    "service": {"name": "unknown", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "8880",
                    "state": {"state": "closed", "reason": "reset", "reason_ttl": "44"},
                    "service": {"name": "cddbp-alt", "method": "table", "conf": "3"}
                }, {
                    "protocol": "udp", "portid": "4445", "state": {
                        "state": "closed", "reason": "port-unreach", "reason_ttl": "44"
                    }, "service": {"name": "upnotifyp", "method": "table", "conf": "3"}
                }, {
                    "protocol": "udp", "portid": "8700", "state": {
                        "state": "closed", "reason": "port-unreach", "reason_ttl": "44"
                    }
                }, {
                    "protocol": "udp", "portid": "8796", "state": {
                        "state": "closed", "reason": "port-unreach", "reason_ttl": "44"
                    }
                }, {
                    "protocol": "udp", "portid": "8798", "state": {
                        "state": "closed", "reason": "port-unreach", "reason_ttl": "44"
                    }, "service": {"name": "unknown", "method": "table", "conf": "3"}
                }, {
                    "protocol": "udp", "portid": "8880", "state": {
                        "state": "closed", "reason": "port-unreach", "reason_ttl": "44"
                    }, "service": {"name": "cddbp-alt", "method": "table", "conf": "3"}
                }]
            }, "times": {"srtt": "86617", "rttvar": "286", "to": "100000"}
        },
    ) | add,
    '51.79.72.209': dict(
        host={
            "starttime": "1611662713", "endtime": "1611732636",
            "status": {"state": "up", "reason": "user-set", "reason_ttl": "0"},
            "address": {"addr": "51.79.72.209", "addrtype": "ipv4"},
            "hostnames": {"hostname": {"name": "ns567760.ip-51-79-72.net", "type": "PTR"}}, "ports": {
                "extraports": [{
                    "state": "closed", "count": "196519",
                    "extrareasons": [{"reason": "aborts", "count": "65535"},
                                     {"reason": "resets", "count": "65516"},
                                     {"reason": "port-unreaches", "count": "65468"}]
                }, {
                    "state": "open|filtered", "count": "67",
                    "extrareasons": {"reason": "no-responses", "count": "67"}
                }],
                "port": [{
                    "protocol": "tcp", "portid": "22",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {"name": "ssh", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "25", "state": {
                        "state": "filtered", "reason": "no-response", "reason_ttl": "0"
                    }, "service": {"name": "smtp", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "80",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {"name": "http", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "443",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {"name": "https", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "1935",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {"name": "rtmp", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "3000",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {"name": "ppp", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "3005",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {"name": "deslogin", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "5060",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {"name": "sip", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "5066",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {"name": "stanag-5066", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "5070",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {"name": "vtsas", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "5080",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {"name": "onscreen", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "5090",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {"name": "unknown", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "7443",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {
                        "name": "oracleas-https", "method": "table", "conf": "3"
                    }
                }, {
                    "protocol": "tcp", "portid": "8021",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {"name": "ftp-proxy", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "8080",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {"name": "http-proxy", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "8081",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {
                        "name": "blackice-icecap", "method": "table", "conf": "3"
                    }
                }, {
                    "protocol": "tcp", "portid": "8082",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {
                        "name": "blackice-alerts", "method": "table", "conf": "3"
                    }
                }, {
                    "protocol": "tcp", "portid": "8888",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {
                        "name": "sun-answerbook", "method": "table", "conf": "3"
                    }
                }, {
                    "protocol": "tcp", "portid": "9999", "state": {
                        "state": "filtered", "reason": "no-response", "reason_ttl": "0"
                    }, "service": {"name": "abyss", "method": "table", "conf": "3"}
                }]
            }, "times": {"srtt": "15359", "rttvar": "534", "to": "100000"}
        },
    ) | add,
    '78.47.226.47': dict(
        host={
            "starttime": "1611663986",
            "endtime": "1611664445",
            "status": {"state": "up", "reason": "user-set", "reason_ttl": "0"},
            "address": {"addr": "78.47.226.47", "addrtype": "ipv4"},
            "hostnames": {"hostname": {"name": "static.107.131.130.94.clients.your-server.de", "type": "PTR"}},
            "ports": {
                "extraports": [{
                    "state": "open|filtered", "count": "131070",
                    "extrareasons": {"reason": "no-responses", "count": "131070"}
                }, {
                    "state": "filtered", "count": "65533",
                    "extrareasons": {"reason": "no-responses", "count": "65533"}
                }],
                "port": [{
                    "protocol": "tcp", "portid": "80",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "44"},
                    "service": {"name": "http", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "443",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "44"},
                    "service": {"name": "https", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "22",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "44"},
                    "service": {"name": "ssh", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "222",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "44"},
                    "service": {"name": "rsh-spx", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "111",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {"name": "rpcbind", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "3128",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {"name": "squid-http", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "8006",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {"name": "wpl-analytics", "method": "table", "conf": "3"}
                }, {
                    "protocol": "udp", "portid": "22", "state": {
                        "state": "closed", "reason": "port-unreach", "reason_ttl": "27"
                    }, "service": {"name": "ssh", "method": "table", "conf": "3"}
                }, {
                    "protocol": "udp", "portid": "80", "state": {
                        "state": "closed", "reason": "port-unreach", "reason_ttl": "27"
                    }, "service": {"name": "http", "method": "table", "conf": "3"}
                }, {
                    "protocol": "udp", "portid": "443", "state": {
                        "state": "closed", "reason": "port-unreach", "reason_ttl": "27"
                    }, "service": {"name": "https", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "4445",
                    "state": {"state": "closed", "reason": "reset", "reason_ttl": "44"},
                    "service": {"name": "upnotifyp", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "8700",
                    "state": {"state": "closed", "reason": "reset", "reason_ttl": "44"}
                }, {
                    "protocol": "tcp", "portid": "8796",
                    "state": {"state": "closed", "reason": "reset", "reason_ttl": "44"}
                }, {
                    "protocol": "tcp", "portid": "8798",
                    "state": {"state": "closed", "reason": "reset", "reason_ttl": "44"},
                    "service": {"name": "unknown", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "8880",
                    "state": {"state": "closed", "reason": "reset", "reason_ttl": "44"},
                    "service": {"name": "cddbp-alt", "method": "table", "conf": "3"}
                }, {
                    "protocol": "udp", "portid": "4445", "state": {
                        "state": "closed", "reason": "port-unreach", "reason_ttl": "44"
                    }, "service": {"name": "upnotifyp", "method": "table", "conf": "3"}
                }, {
                    "protocol": "udp", "portid": "8700", "state": {
                        "state": "closed", "reason": "port-unreach", "reason_ttl": "44"
                    }
                }, {
                    "protocol": "udp", "portid": "8796", "state": {
                        "state": "closed", "reason": "port-unreach", "reason_ttl": "44"
                    }
                }, {
                    "protocol": "udp", "portid": "8798", "state": {
                        "state": "closed", "reason": "port-unreach", "reason_ttl": "44"
                    }, "service": {"name": "unknown", "method": "table", "conf": "3"}
                }, {
                    "protocol": "udp", "portid": "8880", "state": {
                        "state": "closed", "reason": "port-unreach", "reason_ttl": "44"
                    }, "service": {"name": "cddbp-alt", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "25", "state": {
                        "state": "filtered", "reason": "no-response", "reason_ttl": "0"
                    }, "service": {"name": "smtp", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "1935",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {"name": "rtmp", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "3000",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {"name": "ppp", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "3005",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {"name": "deslogin", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "5060",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {"name": "sip", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "5066",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {"name": "stanag-5066", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "5070",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {"name": "vtsas", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "5080",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {"name": "onscreen", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "5090",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {"name": "unknown", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "7443",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {
                        "name": "oracleas-https", "method": "table", "conf": "3"
                    }
                }, {
                    "protocol": "tcp", "portid": "8021",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {"name": "ftp-proxy", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "8080",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {"name": "http-proxy", "method": "table", "conf": "3"}
                }, {
                    "protocol": "tcp", "portid": "8081",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {
                        "name": "blackice-icecap", "method": "table", "conf": "3"
                    }
                }, {
                    "protocol": "tcp", "portid": "8082",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {
                        "name": "blackice-alerts", "method": "table", "conf": "3"
                    }
                }, {
                    "protocol": "tcp", "portid": "8888",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "45"},
                    "service": {
                        "name": "sun-answerbook", "method": "table", "conf": "3"
                    }
                }, {
                    "protocol": "tcp", "portid": "9999", "state": {
                        "state": "filtered", "reason": "no-response", "reason_ttl": "0"
                    }, "service": {"name": "abyss", "method": "table", "conf": "3"}
                }]
            }, "times": {"srtt": "86246", "rttvar": "134", "to": "100000"}
        },
    ) | add,
    # vpn.nferxops.net
    '195.201.240.239': dict(
        host={
            "starttime": "1611733267", "endtime": "1611759507",
            "status": {"state": "up", "reason": "user-set", "reason_ttl": "0"},
            "address": {"addr": "195.201.240.239", "addrtype": "ipv4"},
            "hostnames": {"hostname": {"name": "static.239.240.201.195.clients.your-server.de", "type": "PTR"}},
            "ports": {
                "extraports": [{
                    "state": "open|filtered", "count": "131070",
                    "extrareasons": {"reason": "no-responses", "count": "131070"}
                }, {
                    "state": "filtered", "count": "65535",
                    "extrareasons": {"reason": "no-responses", "count": "65535"}
                }]
            }
        },
    ) | add,
    '4.4.4.4': dict(
        host={
            "starttime": "1611733267",
            "endtime": "1611759507",
            "status": {"state": "up", "reason": "user-set", "reason_ttl": "0"},
            "address": {"addr": "195.201.240.239", "addrtype": "ipv4"},
            "hostnames": {"hostname": {"name": "static.239.240.201.195.clients.your-server.de", "type": "PTR"}},
            "ports": {
                "extraports": [{
                    "state": "open|filtered", "count": "131070",
                    "extrareasons": {"reason": "no-responses", "count": "131070"}
                }, {
                    "state": "filtered", "count": "65535",
                    "extrareasons": {"reason": "no-responses", "count": "65535"}
                }]
            }
        },
    ) | add,
    '8.8.8.8': {
        "scanner": "nmap",
        "args": "nmap -R -r -p- -T4 -oX - -A 144.217.183.113",
        "start": "1602660951",
        "startstr": "Wed Oct 14 07:35:51 2020",
        "version": "7.80",
        "xmloutputversion": "1.04",
        "scaninfo": {"type": "syn", "protocol": "tcp", "numservices": "65535", "services": "1-65535"},
        "verbose": {"level": "0"},
        "debugging": {"level": "0"},
        "host": {
            "starttime": "1602660952", "endtime": "1602673003",
            "status": {"state": "up", "reason": "echo-reply", "reason_ttl": "46"},
            "address": {"addr": "144.217.183.113", "addrtype": "ipv4"},
            "hostnames": {"hostname": {"name": "ns556676.ip-144-217-183.net", "type": "PTR"}},
            "ports": {
                "extraports": {
                    "state": "filtered", "count": "65534",
                    "extrareasons": {"reason": "no-responses", "count": "65534"}
                },
                "port": {
                    "protocol": "tcp",
                    "portid": "80",
                    "state": {"state": "open", "reason": "syn-ack", "reason_ttl": "46"},
                    "service": {
                        "name": "http",
                        "servicefp": "SF-Port80-TCP:V=7.80%I=7%D=10/14%Time=5F86D8B9%P=x86_64-pc-linux-gnu%r("
                                     "GetRequest,C4,"
                                     "\"HTTP/1\\.0\\x20301\\x20Moved\\x20Permanently\\r\\nContent-Type:\\x20text"
                                     "/html;\\x20charset=utf-8\\r\\nLocation:\\x20https:///\\r\\nDate:\\x20Wed,"
                                     "\\x2014\\x20Oct\\x202020\\x2010:53:44\\x20GMT\\r\\nContent-Length:\\x2044"
                                     "\\r\\n\\r\\n<a\\x20href=\\\"https:///\\\">Moved\\x20Permanently</a>\\.\\n"
                                     "\\n\")%r(HTTPOptions,6F,"
                                     "\"HTTP/1\\.0\\x20301\\x20Moved\\x20Permanently\\r\\nLocation:\\x20https"
                                     ":///\\r\\nDate:\\x20Wed,"
                                     "\\x2014\\x20Oct\\x202020\\x2010:53:45\\x20GMT\\r\\nContent-Length:\\x200\\r"
                                     "\\n\\r\\n\")%r(RTSPRequest,67,"
                                     "\"HTTP/1\\.1\\x20400\\x20Bad\\x20Request\\r\\nContent-Type:\\x20text/plain"
                                     ";\\x20charset=utf-8\\r\\nConnection:\\x20close\\r\\n\\r\\n400\\x20Bad"
                                     "\\x20Request\")%r(FourOhFourRequest,10A,"
                                     "\"HTTP/1\\.0\\x20301\\x20Moved\\x20Permanently\\r\\nContent-Type:\\x20text"
                                     "/html;\\x20charset=utf-8\\r\\nLocation:\\x20https:///nice%20ports%2C/Tri"
                                     "%6Eity\\.txt%2ebak\\r\\nDate:\\x20Wed,"
                                     "\\x2014\\x20Oct\\x202020\\x2010:53:55\\x20GMT\\r\\nContent-Length:\\x2079"
                                     "\\r\\n\\r\\n<a\\x20href=\\\"https:///nice%20ports%2C/Tri%6Eity\\.txt%2ebak"
                                     "\\\">Moved\\x20Permanently</a>\\.\\n\\n\")%r(GenericLines,67,"
                                     "\"HTTP/1\\.1\\x20400\\x20Bad\\x20Request\\r\\nContent-Type:\\x20text/plain"
                                     ";\\x20charset=utf-8\\r\\nConnection:\\x20close\\r\\n\\r\\n400\\x20Bad"
                                     "\\x20Request\")%r(Help,67,"
                                     "\"HTTP/1\\.1\\x20400\\x20Bad\\x20Request\\r\\nContent-Type:\\x20text/plain"
                                     ";\\x20charset=utf-8\\r\\nConnection:\\x20close\\r\\n\\r\\n400\\x20Bad"
                                     "\\x20Request\")%r(SSLSessionReq,67,"
                                     "\"HTTP/1\\.1\\x20400\\x20Bad\\x20Request\\r\\nContent-Type:\\x20text/plain"
                                     ";\\x20charset=utf-8\\r\\nConnection:\\x20close\\r\\n\\r\\n400\\x20Bad"
                                     "\\x20Request\")%r(TerminalServerCookie,67,"
                                     "\"HTTP/1\\.1\\x20400\\x20Bad\\x20Request\\r\\nContent-Type:\\x20text/plain"
                                     ";\\x20charset=utf-8\\r\\nConnection:\\x20close\\r\\n\\r\\n400\\x20Bad"
                                     "\\x20Request\")%r(TLSSessionReq,67,"
                                     "\"HTTP/1\\.1\\x20400\\x20Bad\\x20Request\\r\\nContent-Type:\\x20text/plain"
                                     ";\\x20charset=utf-8\\r\\nConnection:\\x20close\\r\\n\\r\\n400\\x20Bad"
                                     "\\x20Request\")%r(Kerberos,67,"
                                     "\"HTTP/1\\.1\\x20400\\x20Bad\\x20Request\\r\\nContent-Type:\\x20text/plain"
                                     ";\\x20charset=utf-8\\r\\nConnection:\\x20close\\r\\n\\r\\n400\\x20Bad"
                                     "\\x20Request\")%r(LPDString,67,"
                                     "\"HTTP/1\\.1\\x20400\\x20Bad\\x20Request\\r\\nContent-Type:\\x20text/plain"
                                     ";\\x20charset=utf-8\\r\\nConnection:\\x20close\\r\\n\\r\\n400\\x20Bad"
                                     "\\x20Request\");",
                        "method": "probed", "conf": "10"
                    },
                    "script": [{
                        "id": "fingerprint-strings",
                        "output": "\n  FourOhFourRequest: \n    HTTP/1.0 301 Moved Permanently\n    "
                                  "Content-Type: text/html; charset=utf-8\n    Location: "
                                  "https:///nice%20ports%2C/Tri%6Eity.txt%2ebak\n    Date: Wed, "
                                  "14 Oct 2020 10:53:55 GMT\n    Content-Length: 79\n    "
                                  "href=\"https:///nice%20ports%2C/Tri%6Eity.txt%2ebak\">Moved "
                                  "Permanently</a>.\n  GenericLines, Help, Kerberos, LPDString, "
                                  "RTSPRequest, SSLSessionReq, TLSSessionReq, TerminalServerCookie: "
                                  "\n    HTTP/1.1 400 Bad Request\n    Content-Type: text/plain; "
                                  "charset=utf-8\n    Connection: close\n    Request\n  GetRequest: "
                                  "\n    HTTP/1.0 301 Moved Permanently\n    Content-Type: "
                                  "text/html; charset=utf-8\n    Location: https:///\n    Date: "
                                  "Wed, 14 Oct 2020 10:53:44 GMT\n    Content-Length: 44\n    "
                                  "href=\"https:///\">Moved Permanently</a>.\n  HTTPOptions: \n    "
                                  "HTTP/1.0 301 Moved Permanently\n    Location: https:///\n    "
                                  "Date: Wed, 14 Oct 2020 10:53:45 GMT\n    Content-Length: 0",
                        "elem": [{
                            "key": "FourOhFourRequest",
                            "#text": "HTTP/1.0 301 Moved Permanently\n    Content-Type: "
                                     "text/html; charset=utf-8\n    Location: "
                                     "https:///nice%20ports%2C/Tri%6Eity.txt%2ebak\n    "
                                     "Date: Wed, 14 Oct 2020 10:53:55 GMT\n    "
                                     "Content-Length: 79\n    "
                                     "href=\"https:///nice%20ports%2C/Tri%6Eity.txt%2ebak\">Moved Permanently</a>."
                        }, {
                            "key": "GenericLines, Help, Kerberos, LPDString, RTSPRequest, "
                                   "SSLSessionReq, TLSSessionReq, TerminalServerCookie",
                            "#text": "HTTP/1.1 400 Bad Request\n    Content-Type: "
                                     "text/plain; charset=utf-8\n    Connection: close\n   "
                                     " Request"
                        }, {
                            "key": "GetRequest",
                            "#text": "HTTP/1.0 301 Moved Permanently\n    Content-Type: "
                                     "text/html; charset=utf-8\n    Location: https:///\n  "
                                     "  Date: Wed, 14 Oct 2020 10:53:44 GMT\n    "
                                     "Content-Length: 44\n    href=\"https:///\">Moved "
                                     "Permanently</a>."
                        }, {
                            "key": "HTTPOptions",
                            "#text": "HTTP/1.0 301 Moved Permanently\n    Location: "
                                     "https:///\n    Date: Wed, 14 Oct 2020 10:53:45 GMT\n "
                                     "   Content-Length: 0"
                        }]
                    }, {
                        "id": "https-redirect",
                        "output": "ERROR: Script execution failed (use -d to debug)"
                    }]
                }
            },
            "os": {
                "portused": {"state": "open", "proto": "tcp", "portid": "80"}, "osmatch": [{
                    "name": "Linux "
                            "2.6.32",
                    "accuracy": "92",
                    "line": "54126",
                    "osclass": {
                        "type":
                            "general "
                            "purpose",
                        "vendor":
                            "Linux",
                        "osfamily":
                            "Linux",
                        "osgen": "2.6.X",
                        "accuracy": "92",
                        "cpe":
                            "cpe:/o:linux:linux_kernel:2.6.32"
                    }
                }, {
                    "name": "Linux "
                            "2.6.32 or"
                            " 3.10",
                    "accuracy": "92",
                    "line": "56650",
                    "osclass": [{
                        "type": "general purpose",
                        "vendor": "Linux",
                        "osfamily": "Linux",
                        "osgen": "2.6.X",
                        "accuracy": "92",
                        "cpe": "cpe:/o:linux:linux_kernel:2.6.32"
                    }, {
                        "type": "general purpose",
                        "vendor": "Linux",
                        "osfamily": "Linux",
                        "osgen": "3.X",
                        "accuracy": "92",
                        "cpe": "cpe:/o:linux:linux_kernel:3.10"
                    }]
                }, {
                    "name": "Linux 4.4",
                    "accuracy": "92",
                    "line": "67202",
                    "osclass": {
                        "type": "general purpose",
                        "vendor": "Linux",
                        "osfamily": "Linux",
                        "osgen": "4.X",
                        "accuracy": "92",
                        "cpe": "cpe:/o:linux:linux_kernel:4.4"
                    }
                }, {
                    "name": "Linux 2.6.32 - 2.6.35",
                    "accuracy": "89",
                    "line": "56133",
                    "osclass": {
                        "type": "general purpose",
                        "vendor": "Linux",
                        "osfamily": "Linux",
                        "osgen": "2.6.X",
                        "accuracy": "89",
                        "cpe": "cpe:/o:linux:linux_kernel:2.6.32"
                    }
                }, {
                    "name": "Linux 2.6.32 - 2.6.39",
                    "accuracy": "89",
                    "line": "56230",
                    "osclass": {
                        "type": "general purpose",
                        "vendor": "Linux",
                        "osfamily": "Linux",
                        "osgen": "2.6.X",
                        "accuracy": "89",
                        "cpe": "cpe:/o:linux:linux_kernel:2.6"
                    }
                }, {
                    "name": "Linux 4.0",
                    "accuracy": "88",
                    "line": "66814",
                    "osclass": {
                        "type": "general purpose",
                        "vendor": "Linux",
                        "osfamily": "Linux",
                        "osgen": "4.X",
                        "accuracy": "88",
                        "cpe": "cpe:/o:linux:linux_kernel:4.0"
                    }
                }, {
                    "name": "Linux 2.6.32 - 3.0",
                    "accuracy": "87",
                    "line": "56293",
                    "osclass": [{
                        "type": "general purpose",
                        "vendor": "Linux",
                        "osfamily": "Linux",
                        "osgen": "2.6.X",
                        "accuracy": "87",
                        "cpe": "cpe:/o:linux:linux_kernel:2.6"
                    }, {
                        "type": "general purpose",
                        "vendor": "Linux",
                        "osfamily": "Linux",
                        "osgen": "3.X",
                        "accuracy": "87",
                        "cpe": "cpe:/o:linux:linux_kernel:3"
                    }]
                }, {
                    "name": "Linux 2.6.18 - 2.6.22",
                    "accuracy": "86",
                    "line": "49721",
                    "osclass": {
                        "type": "general purpose",
                        "vendor": "Linux",
                        "osfamily": "Linux",
                        "osgen": "2.6.X",
                        "accuracy": "86",
                        "cpe": "cpe:/o:linux:linux_kernel:2.6"
                    }
                }, {
                    "name": "Linux 3.10",
                    "accuracy": "86",
                    "line": "62820",
                    "osclass": {
                        "type": "general purpose",
                        "vendor": "Linux",
                        "osfamily": "Linux",
                        "osgen": "3.X",
                        "accuracy": "86",
                        "cpe": "cpe:/o:linux:linux_kernel:3.10"
                    }
                }, {
                    "name": "Linux 3.10 - 4.11",
                    "accuracy": "86",
                    "line": "63230",
                    "osclass": [{
                        "type": "general purpose",
                        "vendor": "Linux",
                        "osfamily": "Linux",
                        "osgen": "3.X",
                        "accuracy": "86",
                        "cpe": "cpe:/o:linux:linux_kernel:3"
                    }, {
                        "type": "general purpose",
                        "vendor": "Linux",
                        "osfamily": "Linux",
                        "osgen": "4.X",
                        "accuracy": "86",
                        "cpe": "cpe:/o:linux:linux_kernel:4"
                    }]
                }]
            },
            "uptime": {"seconds": "425573", "lastboot": "Fri Oct  9 12:43:51 2020"},
            "distance": {"value": "29"},
            "tcpsequence": {
                "index": "260", "difficulty": "Good luck!",
                "values": "F6C1243F,3CE9E56F,78E0D47,7D2CEB56,900387FB,B42B064F"
            },
            "ipidsequence": {"class": "All zeros", "values": "0,0,0,0,0,0"},
            "tcptssequence": {"class": "1000HZ", "values": "195CFCAF,195CFD13,195CFD77,195CFDDB,195CFE40,195CFEA4"},
            "trace": {
                "port": "80", "proto": "tcp", "hop": [{"ttl": "7", "ipaddr": "52.93.29.9", "rtt": "1.91"},
                                                      {"ttl": "11", "ipaddr": "100.91.164.89", "rtt": "110.44"},
                                                      {"ttl": "13", "ipaddr": "100.91.222.77", "rtt": "86.81"},
                                                      {"ttl": "19", "ipaddr": "100.91.56.95", "rtt": "84.42"},
                                                      {"ttl": "20", "ipaddr": "100.100.4.127", "rtt": "85.63"},
                                                      {"ttl": "21", "ipaddr": "100.100.76.196", "rtt": "87.22"},
                                                      {"ttl": "22", "ipaddr": "100.100.84.195", "rtt": "66.28"},
                                                      {"ttl": "23", "ipaddr": "100.100.2.26", "rtt": "84.79"},
                                                      {"ttl": "25", "ipaddr": "192.99.146.138", "rtt": "88.82"}, {
                                                          "ttl": "29", "ipaddr": "144.217.183.113", "rtt": "74.74",
                                                          "host": "ns556676.ip-144-217-183.net"
                                                      }]
            },
            "times": {"srtt": "67514", "rttvar": "66054", "to": "331730"}
        },
        "runstats": {
            "finished": {
                "time": "1602673004", "timestr": "Wed Oct 14 10:56:44 2020", "elapsed": "12052.66",
                "summary": "Nmap done at Wed Oct 14 10:56:44 2020; 1 IP address (1 host up) scanned in 12052.66 "
                           "seconds",
                "exit": "success"
            }, "hosts": {"up": "1", "down": "0", "total": "1"}
        },
    },
}
__all__ = [item for item in globals() if not item.startswith('_') and not inspect.ismodule(globals().get(item))]

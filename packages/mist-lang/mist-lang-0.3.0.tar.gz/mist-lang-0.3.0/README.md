![MIST LOGO](images/logo-yellow-250x250.png)

When you need to create complex Workflows and need to communicate different tools working together, maybe you need `MIST`.

# Why is MIST

`MIST` is a high level programming language for defining executions workflows easily.

Ab execution is a command line tool you can invoke from `MIST`. They will connect the tools and manage executions and synchronization fo you. 

# Installing

```bash
> pip install mist-lang
```

# Quick Start

## Demo 1 - The simplest scenario

**Explanation**

In this scenario we'll do:

1. `CLI Input` - Read a domain as a parameter from CLI.
2. `Search Domains` - Use MIST function for search related domains / sub-domains from a start domain.
3. `Fin OpenPorts` - Search open port for each new domain / sub-domain found.   
4. `Screen (Pring)` - Displays the results into the screen (by using MIST 'print' function). 


**Use case diagram**

![Demo 1](images/mist-demo-1.png)

**MIST code**

```bash
# examples/demo/scenario-01.mist
include "searchDomains" "findOpenPorts"

searchDomains(%domain) => foundDomains

findOpenPorts(:foundDomains, "80,443") => openPortsFound

print(:openPortsFound)
```

**Execute**

```bash
> mist examples/demo/scenario-01.mist domain=example.com
```

## Demo 2 - Sending results to Kafka

**Explanation**

In this scenario we'll do:

1. `CLI Input` - Read a domain as a parameter from CLI.
2. `Search Domains` - Use MIST function for search related domains / sub-domains from a start domain.
3. `FindOpenPorts` - Search open port for each new domain / sub-domain found.   
4. `Kafka output` - Send results to a Kafka topic. 

**Use case diagram**

![Demo 2](images/mist-demo-2.png)

**MIST code**

```bash
# examples/demo/scenario-02.mist
include "searchDomains" "findOpenPorts" "kafkaProducer"

searchDomains(%domain) => foundDomains

findOpenPorts(:foundDomains, "80,443") => openPortsFound

kafkaProducer($KAFKA_SERVER, "domainsTopic", :openPortsFound)
```

**Execute**

```bash
> mist examples/demo/scenario-02.mist domain=example.com
```

## Demo 3 - Adding new tool and remove duplicate domains

**Explanation**

In this scenario we'll do:

1. `CLI Input` - Read a domain as a parameter from CLI.
2. Search domains:
    1. `Search Domains` - Use MIST function for search related domains / sub-domains from a start domain.
    2. `Festin` - Use MIST integration for [Festin](https://github.com/cr0hn/festin) for search related domains / sub-domains from a start domain.
3. `Filter Repeated` - Use MIST function to detect and remove repeated found domains.   
4. `Fin OpenPorts` - Search open port for each new domain / sub-domain get from `Fitler Repeated`.   
5. `Kafka output` - Send results to a Kafka topic.  

**Use case diagram**

![Demo 3](images/mist-demo-3.png)

**MIST code**

```bash
# examples/demo/scenario-03.mist
include "searchDomains" "festin" "findOpenPorts" "filterRepeated" "kafkaProducer"

searchDomains(%domain) => foundDomains
festin(%domain, $DNS_SERVER, True) => foundDomains

filterRepeated(:foundDomains, False) => nonRepeatedFoundDomains

findOpenPorts(:nonRepeatedFoundDomains, "80,443") => openPortsFound

kafkaProducer($KAFKA_SERVER, "domainsTopic", :openPortsFound)

```

**Execute**

```bash
> mist examples/demo/scenario-03.mist domain=example.com
```

## Demo 4 - Send results to Kafka and S3 through a dispatcher

**Explanation**

In this scenario we'll do:

1. `CLI Input` - Read a domain as a parameter from CLI.
2. Search domains:
    1. `Search Domains` - Use MIST function for search related domains / sub-domains from a start domain.
    2. `Festin` - Use MIST integration for [Festin](https://github.com/cr0hn/festin) for search related domains / sub-domains from a start domain.
3. `Filter Repeated` - Use MIST function to detect and remove repeated found domains.   
4. `Find OpenPorts` - Search open port for each new domain / sub-domain get from `Fitler Repeated`.   
5. `Dispatcher (80 / 443)` - Split results and send each port to a different queue.
6. Send results:
    1. `Kafka output` - Send found 80 ports to a Kafka topic.   
    2. `S3 output` - Send found 443 ports to a AWS S3 bucket.   

**Use case diagram**

![Demo 4](images/mist-demo-4.png)

**MIST code**

```bash
# examples/demo/scenario-04.mist
include "searchDomains" "festin" "findOpenPorts" "filterRepeated" "kafkaProducer" "S3Store"

function dispacher(p) {
    if (isEqual(p.port, "80")) {
        send(p, "kafkaOutput")
    } else {
        send(p, "S3Output")
    }
}

searchDomains(%domain) => foundDomains
festin(%domain, $DNS_SERVER, True) => foundDomains

filterRepeated(:foundDomains, False) => nonRepeatedFoundDomains

findOpenPorts(:nonRepeatedFoundDomains, "80,443") => openPortsFound

dispacher(:openPortsFound)

kafkaProducer($KAFKA_SERVER, "domainsTopic", :kafkaOutput)

S3Store(:S3Output, $BUCKET_URI)

```

**Execute**

```bash
> mist examples/demo/scenario-04.mist domain=example.com
```

## Demo 5 - Read from Kafka and a File

**Explanation**

In this scenario we'll do:

1 Input from multiple sources:
   1. `File Input` - Read domains from an external file.
   2. `Kafka Input` - Read domains from Kafka topics.
   3. `CLI Input` - Read domains from CLI.
2. Search domains:
    1. `Search Domains` - Use MIST function for search related domains / sub-domains from a start domain.
    2. `Festin` - Use MIST integration for [Festin](https://github.com/cr0hn/festin) for search related domains / sub-domains from a start domain.
3. `Filter Repeated` - Use MIST function to detect and remove repeated found domains.   
4. `Find OpenPorts` - Search open port for each new domain / sub-domain get from `Fitler Repeated`.   
5. `Dispatcher (80 / 443)` - Split results and send each port to a different queue.
6. Send results:
    1. `Kafka output` - Send found 80 ports to a Kafka topic.   
    2. `S3 output` - Send found 443 ports to a AWS S3 bucket.

**Use case diagram**

![Demo 5](images/mist-demo-5.png)

**MIST code**

```bash
# examples/demo/scenario-05.mist
include "searchDomains" "festin" "findOpenPorts" "filterRepeated" "kafkaProducer" "S3Store" "kafkaConsumer" "tail"

function dispacher(p) {
    if (isEqual(p.port, "80")) {
        send(p, "kafkaOutput")
    } else {
        send(p, "S3Output")
    }
}

kafkaConsumer($KAFKA_SERVER, "inputTopic", "*END*", False) => inputDomains
tail("domains.txt", "*END*") => inputDomains
send(%domain, "inputDomains")

searchDomains(:inputDomains) => foundDomains
festin(:inputDomains, $DNS_SERVER, True) => foundDomains

filterRepeated(:foundDomains, False) => nonRepeatedFoundDomains

findOpenPorts(:nonRepeatedFoundDomains, "80,443") => openPortsFound

dispacher(:openPortsFound)

kafkaProducer($KAFKA_SERVER, "domainsTopic", :kafkaOutput)

S3Store(:S3Output, $BUCKET_URI)
```

**Execute**

```bash
> mist examples/demo/scenario-05.mist domain=example.com
```

## Authors

MIST is being developed by BBVA-Labs Security team members.

## Contributions

Contributions are of course welcome. See [CONTRIBUTING](https://github.com/BBVA/mist/blob/master/CONSTRIBUTING.rst) or skim existing tickets to see where you could help out.

## License

MIST is Open Source Software and available under the [Apache 2 license](https://github.com/BBVA/mist/blob/master/LICENSE)

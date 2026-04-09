---
layout: Conceptual
title: What is Azure Load Balancer? - Azure Load Balancer | Microsoft Learn
canonicalUrl: https://learn.microsoft.com/en-us/azure/load-balancer/load-balancer-overview
breadcrumb_path: /azure/bread/toc.json
feedback_help_link_url: https://learn.microsoft.com/answers/tags/230/azure-load-balancer/
feedback_help_link_type: get-help-at-qna
feedback_product_url: https://feedback.azure.com/d365community/forum/8ae9bf04-8326-ec11-b6e6-000d3a4f0789?c=e8894060-8326-ec11-b6e6-000d3a4f0789
feedback_system: Standard
permissioned-type: public
recommendations: true
recommendation_types:
- Training
- Certification
uhfHeaderId: azure
ms.suite: office
adobe-target: true
author: mbender-ms
learn_banner_products:
- azure
manager: kumud
ms.collection: networking
ms.reviewer: mbender-ms
description: Learn what Azure Load Balancer is, its key features, and how it supports scalable, highly available cloud workloads. Discover scenarios and benefits for your organization.
services: load-balancer
ms.service: azure-load-balancer
ms.topic: overview
ms.date: 2025-07-09T00:00:00.0000000Z
ms.author: mbender
ms.custom: portfolio-consolidation-2025
locale: en-us
document_id: dd59e134-be71-0ac8-bb71-abebb2ef16f5
document_version_independent_id: a99d6a21-1c49-6bfc-9572-f7dfe8be8a4c
updated_at: 2025-10-17T05:14:00.0000000Z
original_content_git_url: https://github.com/MicrosoftDocs/azure-docs-pr/blob/live/articles/load-balancer/load-balancer-overview.md
gitcommit: https://github.com/MicrosoftDocs/azure-docs-pr/blob/18230b48913bac5b413912db38394ed3c1bbabd3/articles/load-balancer/load-balancer-overview.md
git_commit_id: 18230b48913bac5b413912db38394ed3c1bbabd3
site_name: Docs
depot_name: Azure.azure-documents
page_type: conceptual
toc_rel: toc.json
pdf_url_template: https://learn.microsoft.com/pdfstore/en-us/Azure.azure-documents/{branchName}{pdfName}
word_count: 888
asset_id: load-balancer/load-balancer-overview
moniker_range_name: 
monikers: []
item_type: Content
source_path: articles/load-balancer/load-balancer-overview.md
cmProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f98c9a19-e481-4f15-8047-76b641e6ed57
spProducts:
- https://authoring-docs-microsoft.poolparty.biz/devrel/f5685781-a4fd-40f1-8126-59abde4643bf
platformId: 1f761ee6-ffe3-5e83-11ce-5622e044d6e9
---

# What is Azure Load Balancer? - Azure Load Balancer | Microsoft Learn

Important

On September 30, 2025, Basic Load Balancer was retired. For more information, see the [official announcement](https://azure.microsoft.com/updates/azure-basic-load-balancer-will-be-retired-on-30-september-2025-upgrade-to-standard-load-balancer/). If you are currently using Basic Load Balancer, make sure to upgrade to Standard Load Balancer as soon as possible. For guidance on upgrading, visit [Upgrading from Basic Load Balancer - Guidance](load-balancer-basic-upgrade-guidance).

Azure Load Balancer is a cloud service that distributes incoming network traffic across backend virtual machines (VMs) or virtual machine scale sets (VMSS). This article explains Azure Load Balancer's key features, architecture, and scenarios, helping you decide if it fits your organization's load balancing needs for scalable, highly available workloads.

*Load balancing* refers to efficiently distributing incoming network traffic across a group of backend virtual machines (VMs) or virtual machine scale sets (VMSS).

Note

Azure Load Balancer is one of the services that make up the Load Balancing and Content Delivery category in Azure. Other services in this category include [Azure Front Door](../frontdoor/front-door-overview) and [Azure Application Gateway](../application-gateway/overview). Each service has its own unique features and use cases. For more information on this service category, see [Load Balancing and Content Delivery](../networking/load-balancer-content-delivery/load-balancing-content-delivery-overview).

## Load balancer overview

Azure Load Balancer operates at layer 4 of the Open Systems Interconnection (OSI) model. It's the single point of contact for clients. The service distributes inbound flows that arrive at the load balancer's frontend to backend pool instances. These flows are distributed according to configured load-balancing rules and health probes. The backend pool instances can be Azure virtual machines (VMs) or virtual machine scale sets.

A [public load balancer](components#frontend-ip-configurations) can provide both inbound and outbound connectivity for the VMs inside your virtual network. For inbound traffic scenarios, Azure Load Balancer can load balance internet traffic to your VMs. For outbound traffic scenarios, the service can translate the VMs' private IP addresses to public IP addresses for any outbound connections that originate from your VMs.

Alternatively, an [internal (or private) load balancer](components#frontend-ip-configurations) are used to load balance traffic inside a virtual network. With internal load balancer, you can provide inbound connectivity to your VMs in private network connectivity scenarios, such as accessing a load balancer frontend from an on-premises network in a hybrid scenario.

![Screenshot of a diagram showing Azure Load Balancer directing network traffic to backend virtual machines.](media/load-balancer-overview/load-balancer.png)

For more information on the service's individual components, see [Azure Load Balancer components](components).

Azure Load Balancer has three stock-keeping units (SKUs) - Basic, Standard, and Gateway. Each SKU is catered towards a specific scenario and has differences in scale, features, and pricing. For more information, see [Azure Load Balancer SKUs](skus).

## Why use Azure Load Balancer

With Azure Load Balancer, you can scale your applications and create highly available services. The service supports both inbound and outbound scenarios, provides low latency and high throughput, and scales up to millions of flows for all TCP and UDP applications.

### Core capabilities

Azure Load Balancer provides:

- **High availability**: Distribute resources [within](tutorial-load-balancer-standard-public-zonal-portal) and [across](quickstart-load-balancer-standard-public-portal) availability zones
- **Scalability**: Handle millions of flows for TCP and UDP applications
- **Low latency**: Use pass-through load balancing for ultralow latency
- **Flexibility**: Support for [multiple ports, multiple IP addresses, or both](load-balancer-multivip-overview)
- **Health monitoring**: Use [health probes](load-balancer-custom-probe-overview) to ensure traffic is only sent to healthy instances

### Traffic distribution scenarios

- Load balance [internal](quickstart-load-balancer-standard-internal-portal) and [external](quickstart-load-balancer-standard-public-portal) traffic to Azure virtual machines
- Configure [outbound connectivity](load-balancer-outbound-connections) for Azure virtual machines
- Load balance TCP and UDP flow on all ports simultaneously using [high-availability ports](load-balancer-ha-ports-overview)
- Enable [port forwarding](tutorial-load-balancer-port-forwarding-portal) to access virtual machines by public IP address and port

### Advanced features

- **IPv6 support**: Enable [load balancing of IPv6](virtual-network-ipv4-ipv6-dual-stack-standard-load-balancer-powershell) traffic
- **Cross-region mobility**: Move [internal](move-across-regions-internal-load-balancer-portal) and [external](move-across-regions-external-load-balancer-portal) load balancer resources across Azure regions
- **Gateway load balancer integration**: Chain Standard Load Balancer and [Gateway Load Balancer](tutorial-create-gateway-load-balancer)
- **Global load balancing integration**: Distribute traffic [across multiple Azure regions](cross-region-overview) for global applications
- **Admin State**: [Override health probe behavior](manage-admin-state-how-to) for maintenance and operational management

### Monitoring and insights

- **Comprehensive metrics**: Use multidimensional metrics through [Azure Monitor](/en-us/azure/azure-monitor/overview)
- **Pre-built dashboards**: Access [Insights for Azure Load Balancer](load-balancer-insights) with useful visualizations
- **Diagnostics**: Review [Standard load balancer diagnostics](load-balancer-standard-diagnostics) for performance insights
- **Health Event Logs**: Monitor load balancer [health events](load-balancer-health-event-logs) and status changes for proactive management
- **Load Balancer health status**: Gain deeper insights into the health of your load balancer through [health status](load-balancer-manage-health-status) monitoring

### Security features

Azure Load Balancer implements security through multiple layers:

#### Zero Trust security model

- **Standard Load Balancer** is built on the Zero Trust network security model
- Part of your virtual network, which is private and isolated by default

#### Network access controls

- Standard load balancers and public IP addresses are **closed to inbound connections by default**
- **Network Security Groups (NSGs)** must explicitly permit allowed traffic
- Traffic is blocked if no NSG exists on a subnet or NIC

#### Data protection

- Azure Load Balancer **doesn't store customer data**
- All traffic processing happens in real-time without data persistence

Important

Basic Load Balancer is open to the internet by default and will be retired on September 30, 2025. Migrate to Standard Load Balancer for enhanced security.

To learn about NSGs and how to apply them to your scenario, see [Network security groups](../virtual-network/network-security-groups-overview).

## Pricing and SLA

For [Standard Load Balancer](https://github.com/MicrosoftDocs/azure-docs/blob/main/articles/load-balancer/skus.md) pricing information, see [Load Balancer pricing](https://azure.microsoft.com/pricing/details/load-balancer/). For service-level agreements (SLAs), see the [Microsoft licensing information for online services](https://aka.ms/lbsla).

Basic Load Balancer is offered at no charge and has no SLA. It was retired on September 30, 2025.

## What's new?

Subscribe to the RSS feed and view the latest Azure Load Balancer updates on the [Azure Updates](https://azure.microsoft.com/updates?filters=%5B%22Load+Balancer%22%5D) page.
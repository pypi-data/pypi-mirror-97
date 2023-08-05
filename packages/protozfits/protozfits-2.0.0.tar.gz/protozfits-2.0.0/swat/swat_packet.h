/*
 * swat_packet.h
 *
 * Copyright 2019 Jerzy Borkowski/CAMK <jubork@ncac.torun.pl>
 * 
 * The 3-Clause BSD License
 * 
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 * 
 * 1.  Redistributions of source code must retain the above copyright notice,
 * this list of conditions and the following disclaimer.
 * 
 * 2.  Redistributions in binary form must reproduce the above copyright
 * notice, this list of conditions and the following disclaimer in the
 * documentation and/or other materials provided with the distribution.
 * 
 * 3.  Neither the name of the copyright holder nor the names of its
 * contributors may be used to endorse or promote products derived from this
 * software without specific prior written permission.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */

#ifndef SWAT_PACKET_H
#define SWAT_PACKET_H

#include "swat_defs.h"

#include <stddef.h>

#ifdef  __cplusplus
extern "C" {
#endif

#define SWAT_API_PKT_MAGIC0          (0x41)
#define SWAT_API_PKT_MAGIC1          (0x54)

#define SWAT_API_PKTYPE_NULL         (0)
#define SWAT_API_PKTYPE_REQUEST      (1)
#define SWAT_API_PKTYPE_ACCEPT       (2)
#define SWAT_API_PKTYPE_CAMEVS       (3)
#define SWAT_API_PKTYPE_ARREVS       (4)

#define SWAT_API_PKTYPE_MIN         (SWAT_API_PKTYPE_NULL)
#define SWAT_API_PKTYPE_MAX         (SWAT_API_PKTYPE_ARREVS)


/*
Basic chunk of data exchanged between SWAT and CSP/CDTS is packet.
Packet format is :
   
   packet header    (SWAT_PACKET_HEADER - 12 bytes)
   packet payload   (variable number of bytes - lenght specified in packet header)

Types of packets :

SWAT_API_PKTYPE_NULL	- no payload  (0 bytes - SWAT accepts and ignores NULL packets anytime, 
                          excepting very first packet which should be of type SWAT_API_PKTYPE_REQUEST)
SWAT_API_PKTYPE_REQUEST	- payload is SWAT_PKT_REQUEST - very first packet during session. Accepted only once. 
SWAT_API_PKTYPE_ACCEPT	- reply sent back to CSP/CDTS once connection is accepted by SWAT. 
                          If connection is rejected no packet is sent and close() is called
SWAT_API_PKTYPE_CAMEVS	- payload: SWAT_API_PKT_CAMEVHDR + n * SWAT_PACKET_R1_TRIGGER. 
                          Sent periodically by CSP/CDTS to SWAT
SWAT_API_PKTYPE_ARREVS	- payload: n * SWAT_PACKET_R1_EVENT_REQUEST. Sent periodically by SWAT to CSP.

Packet sequencing :

CSP/CDTS -> SWAT :

packet(SWAT_API_PKTYPE_REQUEST, seqnum=0)
packet(SWAT_API_PKTYPE_CAMEVS, seqnum=1)
packet(SWAT_API_PKTYPE_CAMEVS, seqnum=2)
packet(SWAT_API_PKTYPE_CAMEVS, seqnum=3)
[...]

SWAT -> CSP :

packet(SWAT_API_PKTYPE_ACCEPT, seqnum=0)
packet(SWAT_API_PKTYPE_ARREVS, seqnum=1)
packet(SWAT_API_PKTYPE_ARREVS, seqnum=2)
packet(SWAT_API_PKTYPE_ARREVS, seqnum=3)

*/


typedef struct SWAT_PACKET_HEADER_STRUCT
 {
   unsigned char        magic[2];
   unsigned char        telnum;
   unsigned char        pktype;
   unsigned int         seqnum;
   unsigned int         paylen;
 } SWAT_PACKET_HEADER;


typedef struct SWAT_PACKET_CONNECT_STRUCT
 {
   unsigned char  telnum;
   unsigned char	send_flag;	// CSP or CDTS --> SWAT
   unsigned char	recv_flag;	// SWAT --> CSP
   unsigned char	sort_flag;	// CSP/CDTS always sends its trigger strictly sorted
   unsigned char	hw_flag;	// client provides camera triggers from another H/W based array trigger
 } SWAT_PACKET_CONNECT;


typedef struct SWAT_PACKET_R1_TRIGGER_STRUCT{
  uint64_t    		              trigger_id;
  uint8_t     	                trigger_type;
  SWAT_R1_HIGH_RES_TIMESTAMP		trigger_time;
  bool                          readout_requested;
  bool                          data_available;
  uint8_t                       hardware_stereo_trigger_mask;
  
  // Proposed in the old protocol version; use was generic
  // the value was never read
  //unsigned int		counter1;
  //unsigned int		counter2;  
} SWAT_PACKET_R1_TRIGGER;


typedef struct SWAT_PACKET_R1_EVENT_REQUEST_STRUCT{
  unsigned int			      assigned_event_id;
  SWAT_PACKET_R1_TRIGGER	requested;

  // Outside of R1 spec: field required to support negative triggers
  unsigned char		        negative_flag;

} SWAT_PACKET_R1_EVENT_REQUEST;


int     swat_pkthdr_check_common(SWAT_PACKET_HEADER *pkthdr);
int     swat_pkthdr_check_send(SWAT_PACKET_HEADER *pkthdr);
int     swat_pkthdr_check_recv(SWAT_PACKET_HEADER *pkthdr);
int     swat_pkthdrtype_check_send(SWAT_PACKET_HEADER *pkthdr, int pktype);
int     swat_pkthdrtype_check_recv(SWAT_PACKET_HEADER *pkthdr, int pktype);
int	swat_pkt_arrev_log(SWAT_PACKET_HEADER *ph);

#ifdef  __cplusplus
}
#endif

#endif /* SWAT_PACKET_H */

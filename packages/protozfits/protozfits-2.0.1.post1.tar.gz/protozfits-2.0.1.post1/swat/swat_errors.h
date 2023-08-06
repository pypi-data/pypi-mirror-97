/*
 * swat_errors.h
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

#ifndef SWAT_ERRORS_H
#define SWAT_ERRORS_H

#define SWAT_OK				(0)

#define SWAT_ERR_BASE			(50)

#define SWAT_ERR_BAD_CMDLINE            (SWAT_ERR_BASE + 0)
#define SWAT_ERR_BAD_ARG                (SWAT_ERR_BASE + 1)
#define SWAT_ERR_NUL_PTR                (SWAT_ERR_BASE + 2)
#define SWAT_ERR_NO_LOGFILE             (SWAT_ERR_BASE + 3)
#define SWAT_ERR_NUL_LOG_MSG            (SWAT_ERR_BASE + 4)
#define SWAT_ERR_BAD_LOG_MSG_TYPE       (SWAT_ERR_BASE + 5)
#define SWAT_ERR_BAD_HANDLE  		(SWAT_ERR_BASE + 6)
#define SWAT_ERR_SOCKET_HANGUP          (SWAT_ERR_BASE + 7)
#define SWAT_ERR_EXITING                (SWAT_ERR_BASE + 8)
#define SWAT_ERR_NO_NEW_DATA            (SWAT_ERR_BASE + 9)
#define SWAT_ERR_WRITE_FAILED           (SWAT_ERR_BASE + 10)
#define SWAT_ERR_READ_FAILED            (SWAT_ERR_BASE + 11)
#define SWAT_BIG_ENDIAN                 (SWAT_ERR_BASE + 12)
#define SWAT_LITTLE_ENDIAN              (SWAT_ERR_BASE + 13)
#define SWAT_ERR_UNKNOWN_ENDIAN         (SWAT_ERR_BASE + 14)
#define SWAT_ERR_PTHREAD_CREATE_FAILED  (SWAT_ERR_BASE + 15)
#define SWAT_ERR_NO_SOCKET              (SWAT_ERR_BASE + 16)
#define SWAT_ERR_CONNECT_FAILED         (SWAT_ERR_BASE + 17)
#define SWAT_ERR_FCNTL_FAILED           (SWAT_ERR_BASE + 18)
#define SWAT_ERR_MALLOC_FAILED          (SWAT_ERR_BASE + 19)
#define SWAT_ERR_MUTEX_INIT_FAILED      (SWAT_ERR_BASE + 20)
#define SWAT_ERR_INQUE_FULL             (SWAT_ERR_BASE + 21)
#define SWAT_ERR_INQUE_NOT_RESERVED     (SWAT_ERR_BASE + 22)
#define SWAT_ERR_INQUE_NOT_FREE         (SWAT_ERR_BASE + 23)
#define SWAT_ERR_NOT_FOUND              (SWAT_ERR_BASE + 24)
#define SWAT_ERR_NOT_EMPTY              (SWAT_ERR_BASE + 25)
#define SWAT_ERR_SLOT_OCCUPIED          (SWAT_ERR_BASE + 26)
#define SWAT_ERR_SLOT_EMPTY             (SWAT_ERR_BASE + 27)
#define SWAT_ERR_NOT_ENABLED            (SWAT_ERR_BASE + 28)
#define SWAT_ERR_NOT_SAME_SUBARR        (SWAT_ERR_BASE + 29)
#define SWAT_WARN_TRUNCATED             (SWAT_ERR_BASE + 30)
#define SWAT_ERR_INTERNAL               (SWAT_ERR_BASE + 31)
#define SWAT_ERR_TOO_LATE               (SWAT_ERR_BASE + 32)
#define SWAT_ERR_TOO_EARLY              (SWAT_ERR_BASE + 33)
#define SWAT_ERR_BUF_OVERFLOW		(SWAT_ERR_BASE + 34)
#define SWAT_ERR_TOO_MANY		(SWAT_ERR_BASE + 35)
#define SWAT_ERR_BAD_MAGIC0		(SWAT_ERR_BASE + 36)
#define SWAT_ERR_BAD_MAGIC1		(SWAT_ERR_BASE + 37)
#define SWAT_ERR_BAD_PKTYPE		(SWAT_ERR_BASE + 38)
#define SWAT_ERR_BAD_CSID		(SWAT_ERR_BASE + 39)
#define SWAT_ERR_BAD_PAYLEN		(SWAT_ERR_BASE + 40)
#define SWAT_ERR_SOCKET_FAILED		(SWAT_ERR_BASE + 41)
#define SWAT_ERR_DISCARDED		(SWAT_ERR_BASE + 42)
#define SWAT_ERR_BIND_FAILED		(SWAT_ERR_BASE + 43)
#define SWAT_ERR_LISTEN_FAILED		(SWAT_ERR_BASE + 44)
#define SWAT_ERR_SETNONBLOCK_FAILED	(SWAT_ERR_BASE + 45)
#define SWAT_ERR_EPOLL_CREATE_FAILED	(SWAT_ERR_BASE + 46)
#define SWAT_ERR_EPOLL_CTL_FAILED	(SWAT_ERR_BASE + 47)
#define SWAT_ERR_BAD_PROTOCOL		(SWAT_ERR_BASE + 48)
#define SWAT_ERR_ALLOC_HANDLE_FAILED	(SWAT_ERR_BASE + 49)
#define SWAT_ERR_ACCEPT_FAILED		(SWAT_ERR_BASE + 50)
#define SWAT_ERR_NO_TELESCOPE		(SWAT_ERR_BASE + 51)
#define SWAT_ERR_PKT_TOO_LONG		(SWAT_ERR_BASE + 52)
#define SWAT_ERR_BAD_STATE		(SWAT_ERR_BASE + 53)
#define SWAT_ERR_TIMEOUT		(SWAT_ERR_BASE + 54)
#define SWAT_ERR_EPOLL_WAIT_FAILED	(SWAT_ERR_BASE + 55)
#define SWAT_ERR_NO_MEMORY		(SWAT_ERR_BASE + 56)
#define	SWAT_ERR_ALREADY_SETUP		(SWAT_ERR_BASE + 57)
#define	SWAT_ERR_BUFFER_FULL		(SWAT_ERR_BASE + 58)
#define	SWAT_ERR_BAD_WR_SEQNUM		(SWAT_ERR_BASE + 59)
#define	SWAT_ERR_BAD_RD_SEQNUM		(SWAT_ERR_BASE + 60)
#define	SWAT_ERR_GETTIME_FAILED		(SWAT_ERR_BASE + 61)
#define	SWAT_ERR_TAI_NOT_VALID		(SWAT_ERR_BASE + 62)
#define	SWAT_ERR_CANNOT_CALIBRATE	(SWAT_ERR_BASE + 63)
#define	SWAT_ERR_SETKEEPALIVE_FAILED	(SWAT_ERR_BASE + 64)
#define	SWAT_ERR_CFG_OVERWRITTEN	(SWAT_ERR_BASE + 65)
#define	SWAT_ERR_NOT_SAME_CONFIG	(SWAT_ERR_BASE + 66)
#define	SWAT_ERR_CFG_COMPATIBLE		(SWAT_ERR_BASE + 67)

#endif /* SWAT_ERRORS_H */


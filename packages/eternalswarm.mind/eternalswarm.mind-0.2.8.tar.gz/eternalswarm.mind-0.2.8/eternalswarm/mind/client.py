from typing import List, Optional, TextIO, Tuple

import grpc

from . import (bloodhound_pb2, bloodhound_pb2_grpc, callback_pb2,
               callback_pb2_grpc, cracker_pb2, cracker_pb2_grpc,
               exploitation_pb2, exploitation_pb2_grpc,
               information_pb2, information_pb2_grpc, metasploit_pb2,
               metasploit_pb2_grpc, models_pb2, relaying_pb2,
               relaying_pb2_grpc, scanner_pb2, scanner_pb2_grpc, terminal_pb2,
               terminal_pb2_grpc, wireguard_pb2, wireguard_pb2_grpc)


class Client():

    def __init__(self, ip: str, port: int, ssl: bool = False, ca: str = None, cert: str = None, key: str = None):
        self.ip = ip
        self.port = port
        self.ssl = ssl
        self.ca = ca
        self.cert = cert
        self.key = key
        self._channel = None
        self.uid = ''

    @property
    def channel(self):
        """
            Channel and stuff...
        """
        if self._channel is None:
            if self.ssl:
                credentials = grpc.ssl_channel_credentials(
                    self.ca, self.key, self.cert
                )
                options = ()
                if self.uid:
                    options = (
                        ('grpc.ssl_target_name_override', self.uid,),
                    )
                self._channel = grpc.secure_channel(
                    f"{self.ip}:{self.port}",
                    credentials,
                    options=options
                )
            else:
                self._channel = grpc.insecure_channel(
                    f"{self.ip}:{self.port}"
                )
        return self._channel

    def _perform_request(self, function, call_arguments):
        """
            Perform the request, this function will raise Exceptions and return the result otherwise.
        """
        try:
            return function(call_arguments)
        except grpc._channel._Rendezvous as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                self._channel.close()
                self._channel = None
            raise e
        except Exception as e:
            self._channel = None
            raise e

    def perform_request(self, function, call_arguments):
        """
            Perform the request
        """
        return self._perform_request(function, call_arguments)

    def reset_stubs(self):
        """Reset the stubs with the new information"""
        raise NotImplementedError("Should be overwritten!")

    @staticmethod
    def create_pagination_message(scan_id: int, **kwargs) -> models_pb2.Pagination:
        """
            Create a pagination message from the given arguments.
        """
        scan = models_pb2.Scan(id=scan_id)
        pagination = models_pb2.Pagination(scan=scan)
        for key, value in kwargs.items():
            try:
                setattr(pagination, key, value)
            except AttributeError:
                pass
        return pagination


class DroneClient(Client):
    """
        Client class to talk with drones.
    """

    def __init__(self, uid: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uid = uid

        self.scanner_stub = scanner_pb2_grpc.ScannerStub(self.channel)
        self.exploit_stub = exploitation_pb2_grpc.ExploitServiceStub(
            self.channel
        )
        self.info_stub = information_pb2_grpc.InformationStub(self.channel)
        self.bloodhound_stub = bloodhound_pb2_grpc.BloodHoundStub(self.channel)
        self.relaying_stub = relaying_pb2_grpc.RelayingStub(self.channel)
        self.metasploit_stub = metasploit_pb2_grpc.MetasploitStub(self.channel)
        self.terminal_stub = terminal_pb2_grpc.TerminalServiceStub(self.channel)

    def reset_stubs(self):
        """Reset the stubs"""
        self.scanner_stub = scanner_pb2_grpc.ScannerStub(self.channel)
        self.exploit_stub = exploitation_pb2_grpc.ExploitServiceStub(
            self.channel
        )
        self.info_stub = information_pb2_grpc.InformationStub(self.channel)
        self.bloodhound_stub = bloodhound_pb2_grpc.BloodHoundStub(self.channel)
        self.relaying_stub = relaying_pb2_grpc.RelayingStub(self.channel)
        self.metasploit_stub = metasploit_pb2_grpc.MetasploitStub(self.channel)
        self.terminal_stub = terminal_pb2_grpc.TerminalServiceStub(
            self.channel
        )

    def ping(self):
        """Ping"""
        return self.perform_request(
            self.info_stub.Ping,
            information_pb2.PingMessage(
                ping="test"
            )
        )

    def get_info(self):
        """
            Get some generic info from the device like ip and version numbers.
        """
        return self.perform_request(
            self.info_stub.GetInfo,
            information_pb2.InfoRequest(filter=information_pb2.InfoRequest.ALL)
        )

    def get_settings(self):
        """
            Get the settings list.
        """
        return self.perform_request(self.info_stub.GetSettings, information_pb2.SettingsRequest())

    def set_setting(self, section, key, value):
        """
            Change a setting of a key to value.
        """
        section_pb2 = information_pb2.Section(name=section)
        setting_pb2 = section_pb2.settings.add()
        setting_pb2.key = key
        setting_pb2.value = value
        return self.perform_request(self.info_stub.SetSetting, section_pb2)

    def enable_ssl(self, cert: str, key: str, ca: str):
        """Enable SSL on the drone grpc socket."""
        request = information_pb2.Certificates(
            cert=cert,
            key=key,
            ca=ca
        )
        return self.perform_request(
            self.info_stub.EnableGRPCSSL,
            request
        )

    def set_callback_certs(self, host: str, port: int, cert: str, key: str, ca: str):
        """Enable SSL on the drone grpc socket."""
        request = information_pb2.Certificates(
            cert=cert,
            key=key,
            ca=ca,
            host=host,
            port=port,
        )
        return self.perform_request(
            self.info_stub.SetCallbackCerts,
            request
        )

    def restart_drone(self):
        """Restart the drone"""
        return self.perform_request(
            self.info_stub.RestartServices,
            information_pb2.RestartMessage()
        )

    def get_drone_capabilities(self):
        """Get the capabilities of the drone"""
        return self.perform_request(
            self.info_stub.GetDroneCapabilities,
            models_pb2.EmptyMessage()
        )

    def list_scans(self):
        """
            List all the scans
        """
        return self.perform_request(self.scanner_stub.ListScans, scanner_pb2.ScanListRequest())

    def create_scan(self, name: str, description: str, targets: List[str], ping: bool):
        """
            Create a new scan.
        """
        scan = models_pb2.Scan(name=name, description=description)
        for target in targets:
            pb_target = scan.targets.add()
            pb_target.address = target
            pb_target.ping = ping
        return self.perform_request(self.scanner_stub.CreateScan, scan)

    def update_scan(self, scan_id: int, name: str, description: str):
        """Update the name and description of a scan"""
        scan = models_pb2.Scan(id=scan_id, name=name, description=description)
        return self.perform_request(self.scanner_stub.UpdateScan, scan)

    def delete_scan(self, scan_id: int):
        """Update the name and description of a scan"""
        scan = models_pb2.Scan(id=scan_id)
        return self.perform_request(self.scanner_stub.DeleteScan, scan)

    def add_targets(self, scan_id: int, targets: List[str], ping: bool):
        """
            Add new targets to an existing scan.
        """
        scan = models_pb2.Scan(id=scan_id)
        for target in targets:
            pb_target = scan.targets.add()
            pb_target.address = target
            pb_target.ping = ping
        return self.perform_request(self.scanner_stub.AddTargets, scan)

    def list_hosts(self, pagination: models_pb2.Pagination):
        """
            List the hosts with the given pagination.
        """
        return self.perform_request(self.scanner_stub.ListHosts, pagination)

    def list_host_filters(self, scan_id: int):
        return self.perform_request(
            self.scanner_stub.ListHostFilters,
            models_pb2.Scan(id=scan_id)
        )

    def get_host(self, host_id: int):
        """Retrieve a single host"""
        return self.perform_request(
            self.scanner_stub.GetHost,
            scanner_pb2.GetRequest(id=host_id)
        )

    def list_services(self, pagination: models_pb2.Pagination):
        return self.perform_request(self.scanner_stub.ListServices, pagination)

    def get_service(self, service_id: int):
        return self.perform_request(
            self.scanner_stub.GetService,
            scanner_pb2.GetRequest(id=service_id)
        )

    def list_service_filters(self, scan_id: int):
        return self.perform_request(
            self.scanner_stub.ListServiceFilters,
            models_pb2.Scan(id=scan_id)
        )

    def list_vulnerabilities(self, pagination: models_pb2.Pagination):
        return self.perform_request(self.scanner_stub.ListVulns, pagination)

    def list_vulnerability_filters(self, scan_id: int):
        return self.perform_request(
            self.scanner_stub.ListVulnFilters,
            models_pb2.Scan(id=scan_id)
        )

    def list_exploits(self, pagination: models_pb2.Pagination):
        return self.perform_request(self.scanner_stub.ListExploits, pagination)

    def get_exploit(self, exploit_id: int):
        return self.perform_request(
            self.scanner_stub.GetExploit,
            scanner_pb2.GetRequest(id=exploit_id)
        )

    def list_exploit_filters(self, scan_id: int):
        return self.perform_request(
            self.scanner_stub.ListExploitFilters,
            models_pb2.Scan(id=scan_id)
        )

    def list_credentials(self, pagination: models_pb2.Pagination):
        return self.perform_request(self.scanner_stub.ListCredentials, pagination)

    def get_credential(self, credential_id: int):
        return self.perform_request(
            self.scanner_stub.GetCredential,
            scanner_pb2.GetRequest(id=credential_id)
        )

    def list_credential_filters(self, scan_id: int):
        return self.perform_request(
            self.scanner_stub.ListCredentialFilters,
            models_pb2.Scan(id=scan_id)
        )

    def list_targets(self, pagination: models_pb2.Pagination):
        return self.perform_request(self.scanner_stub.ListTargets, pagination)

    def scan_stats(self, scan_id: int):
        return self.perform_request(self.scanner_stub.GetStats, models_pb2.Scan(id=scan_id))

    def pin_object(self, host_id: int = 0, service_id: int = 0, credential_id: int = 0, user_id: int = 0,
                   group_id: int = 0, domain_id: int = 0, file_id: int = 0, hash_id: int = 0):
        """Pin an object to the top of the list"""
        return self.perform_request(
            self.scanner_stub.PinObject,
            scanner_pb2.PinMessage(
                host_id=host_id,
                service_id=service_id,
                credential_id=credential_id,
                user_id=user_id,
                group_id=group_id,
                domain_id=domain_id,
                file_id=file_id,
                hash_id=hash_id,
            )
        )

    def list_loot_modules(self):
        return self.perform_request(self.exploit_stub.ListLootModules, models_pb2.EmptyRequest())

    def list_login_modules(self):
        return self.perform_request(self.exploit_stub.ListLoginModules, models_pb2.EmptyRequest())

    def exploit(self, vuln_id, exploit_id: str, credential_id: int, payload_id: str = ''):
        request = exploitation_pb2.ExploitRequest(
            vulnerability_id=vuln_id,
            exploit_id=exploit_id
        )
        if credential_id:
            request.credential.CopyFrom(
                models_pb2.Credential(id=credential_id)
            )
        if payload_id:
            request.payload.CopyFrom(
                models_pb2.Payload(id=payload_id)
            )
        return self.perform_request(self.exploit_stub.PerformExploit, request)

    def list_loot(self, pagination: models_pb2.Pagination):
        return self.perform_request(self.scanner_stub.ListLoot, pagination)

    def get_loot(self, loot_id: int):
        return self.perform_request(
            self.scanner_stub.GetLoot,
            scanner_pb2.GetRequest(id=loot_id)
        )

    def list_loot_filters(self, scan_id: int):
        return self.perform_request(
            self.scanner_stub.ListLootFilters,
            models_pb2.Scan(id=scan_id)
        )

    def loot(self, service_id: int, credential_id: int, module_name: str):
        request = exploitation_pb2.LootRequest(
            service_id=service_id,
            credential_id=credential_id,
            module_name=module_name
        )
        return self.perform_request(self.exploit_stub.PerformLoot, request)

    def multi_loot(self, scan_id: int, credential_id: int, module_name: str, domain_id: int, port: int, max_number: int,
                   not_looted: bool, admin_only: bool = False):
        request = exploitation_pb2.LootRequest(
            credential_id=credential_id,
            module_name=module_name,
            domain_id=domain_id,
            port=port,
            max_loot=max_number,
            only_not_looted=not_looted,
            scan_id=scan_id,
            admin_only=admin_only,
        )
        return self.perform_request(self.exploit_stub.PerformMultipleLoot, request)

    def cancel_loot(self, loot_id: int = 0):
        request = exploitation_pb2.CancelRequest(
            id=loot_id,
        )
        return self.perform_request(self.exploit_stub.CancelLoot, request)

    def cancel_exploit(self, exploit_id: int = 0):
        request = exploitation_pb2.CancelRequest(
            id=exploit_id,
        )
        return self.perform_request(self.exploit_stub.CancelExploit, request)

    def list_discovery(self, pagination: models_pb2.Pagination):
        return self.perform_request(self.scanner_stub.ListDiscovery, pagination)

    def list_discovery_modules(self):
        return self.perform_request(self.scanner_stub.ListDiscoveryModules, models_pb2.EmptyRequest())

    def create_discovery(self, scan_id: int, ping: bool, modules: List[str]):
        discovery = models_pb2.Discovery(
            scan_id=scan_id,
            ping=ping,
            modules=modules
        )
        return self.perform_request(self.scanner_stub.StartDiscovery, discovery)

    def cancel_discovery(self, discovery_id: int):
        return self.perform_request(
            self.scanner_stub.CancelDiscovery,
            models_pb2.Discovery(
                id=discovery_id,
            )
        )

    def list_sessions(self, pagination: models_pb2.Pagination):
        return self.perform_request(self.scanner_stub.ListSession, pagination)

    def get_session(self, session_id: int):
        return self.perform_request(
            self.scanner_stub.GetSession,
            models_pb2.Scan(id=session_id)
        )

    def list_session_filters(self, scan_id: int):
        return self.perform_request(
            self.scanner_stub.ListSessionFilters,
            models_pb2.Scan(id=scan_id)
        )

    def list_local_admins(self, pagination: models_pb2.Pagination):
        return self.perform_request(self.scanner_stub.ListLocalAdmins, pagination)

    def get_local_admin(self, admin_id: int):
        return self.perform_request(
            self.scanner_stub.GetLocalAdmin,
            models_pb2.Scan(id=admin_id)
        )

    def list_local_admin_filters(self, scan_id: int):
        return self.perform_request(
            self.scanner_stub.ListLocalAdminFilters,
            models_pb2.Scan(id=scan_id)
        )

    def get_relaying_status(self):
        return self.perform_request(
            self.relaying_stub.GetStatus,
            relaying_pb2.RelayingRequest()
        )

    def list_relaying_targets(self, pagination: models_pb2.Pagination):
        return self.perform_request(
            self.scanner_stub.ListRelayingTargets,
            pagination
        )

    def list_relaying_log(self, pagination: models_pb2.Pagination):
        return self.perform_request(
            self.scanner_stub.ListRelayingLog,
            pagination
        )

    def start_responder(self, scan_id: int, arguments: str = ''):
        return self.perform_request(
            self.relaying_stub.StartResponder,
            relaying_pb2.StartMessage(scan_id=scan_id, arguments=arguments)
        )

    def add_relaying_target(self, scan_id: int, service_id: int = 0, target_string: str = ''):
        return self.perform_request(
            self.relaying_stub.AddRelayingTarget,
            models_pb2.RelayingTarget(scan_id=scan_id, service_id=service_id, target_string=target_string)
        )

    def remove_relaying_target(self, target_string: str):
        return self.perform_request(
            self.relaying_stub.RemoveRelayingTarget,
            models_pb2.RelayingTarget(target_string=target_string)
        )

    def sync_relaying_targets(self):
        return self.perform_request(
            self.relaying_stub.SyncRelayingTargets,
            relaying_pb2.Response()
        )

    def clear_relaying_targets(self):
        return self.perform_request(
            self.relaying_stub.ClearRelayingTargets,
            relaying_pb2.Response()
        )

    def start_mitm6(self, scan_id: int, arguments: str = ''):
        return self.perform_request(
            self.relaying_stub.StartMitm6,
            relaying_pb2.StartMessage(scan_id=scan_id, arguments=arguments)
        )

    def start_relaying(self, scan_id: int, arguments: str = ''):
        return self.perform_request(
            self.relaying_stub.StartRelaying,
            relaying_pb2.StartMessage(scan_id=scan_id, arguments=arguments)
        )

    def stop_responder(self, scan_id: int):
        return self.perform_request(
            self.relaying_stub.StopResponder,
            relaying_pb2.StopMessage()
        )

    def stop_mitm6(self, scan_id: int):
        return self.perform_request(
            self.relaying_stub.StopMitm6,
            relaying_pb2.StopMessage()
        )

    def stop_relaying(self, scan_id: int):
        return self.perform_request(
            self.relaying_stub.StopRelaying,
            relaying_pb2.StopMessage()
        )

    def get_responder_output(self):
        return self.perform_request(
            self.relaying_stub.GetResponderOutput,
            relaying_pb2.OutputRequest()
        )

    def get_mitm6_output(self):
        return self.perform_request(
            self.relaying_stub.GetMitm6Output,
            relaying_pb2.OutputRequest()
        )

    def get_relaying_output(self):
        return self.perform_request(
            self.relaying_stub.GetRelayingOutput,
            relaying_pb2.OutputRequest()
        )

    def list_files(self, pagination: models_pb2.Pagination):
        return self.perform_request(self.scanner_stub.ListFiles, pagination)

    def get_file(self, file_id: int):
        return self.perform_request(
            self.scanner_stub.GetFile,
            scanner_pb2.GetRequest(id=file_id)
        )

    def list_file_filters(self, scan_id: int):
        return self.perform_request(
            self.scanner_stub.ListFileFilters,
            models_pb2.Scan(id=scan_id)
        )

    def stream_image(self, file_id: int):
        for chunk in self.scanner_stub.GetFileStream(models_pb2.File(id=file_id)):
            yield chunk.chunk

    def add_credential(self, scan_id: int, username: str, password: str, domain: str, domain_id: int, lm: str, nt: str,
                       credential_type: int = 0):
        credential = models_pb2.Credential(
            password=password, lm=lm, nt=nt, scan_id=scan_id, cred_type=credential_type  # type: ignore
        )
        credential.user.MergeFrom(models_pb2.User(username=username))
        if domain or domain_id:
            credential.domain.MergeFrom(
                models_pb2.Domain(id=domain_id, dns_name=domain)
            )
        return self.perform_request(self.scanner_stub.AddCredential, credential)

    @staticmethod
    def list_credential_types():
        entries = []
        for key, value in models_pb2.CredentialType.items():
            if value > 0:
                entries.append(dict(key=key, value=value))
        return dict(entries=entries)

    def change_credential(self, credential_id: int, username: str = '', password: str = '', domain: str = '',
                          domain_id: int = 0, lm: str = '', nt: str = '',
                          credential_type: int = 0):
        credential = models_pb2.Credential(
            password=password, lm=lm, nt=nt, id=credential_id, cred_type=credential_type  # type: ignore
        )
        credential.user.MergeFrom(models_pb2.User(username=username))
        credential.user.MergeFrom(models_pb2.User(username=username))
        if domain or domain_id:
            credential.domain.MergeFrom(
                models_pb2.Domain(id=domain_id, dns_name=domain)
            )
        return self.perform_request(self.scanner_stub.ChangeCredential, credential)

    def list_out_of_scope(self, pagination: models_pb2.Pagination):
        return self.perform_request(
            self.scanner_stub.ListOutOfScope,
            pagination
        )

    def add_out_of_scope(self, scan_id: int, ip_range: str, description: str):
        return self.perform_request(
            self.scanner_stub.AddOutOfScope,
            models_pb2.OutOfScope(
                scan_id=scan_id,
                ip_range=ip_range,
                description=description)
        )

    def get_log(self, log_id: int):
        return self.perform_request(
            self.scanner_stub.GetLog,
            scanner_pb2.GetRequest(id=log_id)
        )

    def list_domains(self, pagination: models_pb2.Pagination):
        return self.perform_request(self.scanner_stub.ListDomains, pagination)

    def get_domain(self, domain_id: int):
        return self.perform_request(
            self.scanner_stub.GetDomain,
            scanner_pb2.GetRequest(id=domain_id)
        )

    def list_domain_filters(self, scan_id: int):
        return self.perform_request(
            self.scanner_stub.ListDomainFilters,
            models_pb2.Scan(id=scan_id)
        )

    def get_application_log(self, log_type, start: int, count: int):
        return self.perform_request(
            self.info_stub.GetLog,
            information_pb2.LogRequest(
                start=start,
                count=count,
                type=log_type
            )
        )

    def list_users(self, pagination: models_pb2.Pagination):
        return self.perform_request(self.scanner_stub.ListUsers, pagination)

    def get_user(self, user_id: int):
        return self.perform_request(
            self.scanner_stub.GetUser,
            scanner_pb2.GetRequest(id=user_id)
        )

    def list_user_filters(self, scan_id: int):
        return self.perform_request(
            self.scanner_stub.ListUserFilters,
            models_pb2.Scan(id=scan_id)
        )

    def list_groups(self, pagination: models_pb2.Pagination):
        return self.perform_request(self.scanner_stub.ListGroups, pagination)

    def get_group(self, group_id: int):
        return self.perform_request(
            self.scanner_stub.GetGroup,
            scanner_pb2.GetRequest(id=group_id)
        )

    def list_group_filters(self, scan_id: int):
        return self.perform_request(
            self.scanner_stub.ListGroupFilters,
            models_pb2.Scan(id=scan_id)
        )

    def list_group_memberships(self, pagination: models_pb2.Pagination):
        return self.perform_request(self.scanner_stub.ListGroupMemberships, pagination)

    def get_group_membership(self, membership_id: int):
        return self.perform_request(
            self.scanner_stub.GetGroupMembership,
            scanner_pb2.GetRequest(id=membership_id)
        )

    def list_group_membership_filters(self, scan_id: int):
        return self.perform_request(
            self.scanner_stub.ListGroupMembershipFilters,
            models_pb2.Scan(id=scan_id)
        )

    def list_trusts(self, pagination: models_pb2.Pagination):
        return self.perform_request(self.scanner_stub.ListTrusts, pagination)

    def get_trust(self, trust_id: int):
        return self.perform_request(
            self.scanner_stub.GetTrust,
            scanner_pb2.GetRequest(id=trust_id)
        )

    def list_trust_filters(self, scan_id: int):
        return self.perform_request(
            self.scanner_stub.ListTrustFilters,
            models_pb2.Scan(id=scan_id)
        )

    def list_policies(self, pagination: models_pb2.Pagination):
        return self.perform_request(self.scanner_stub.ListPolicies, pagination)

    def get_policy(self, trust_id: int):
        return self.perform_request(
            self.scanner_stub.GetPolicy,
            scanner_pb2.GetRequest(id=trust_id)
        )

    def list_policy_filters(self, scan_id: int):
        return self.perform_request(
            self.scanner_stub.ListPolicyFilters,
            models_pb2.Scan(id=scan_id)
        )

    def list_hashes(self, pagination: models_pb2.Pagination):
        return self.perform_request(self.scanner_stub.ListHashes, pagination)

    def get_hash(self, hash_id: int):
        return self.perform_request(
            self.scanner_stub.GetHash,
            scanner_pb2.GetRequest(id=hash_id)
        )

    def list_hash_filters(self, scan_id: int):
        return self.perform_request(
            self.scanner_stub.ListHashFilters,
            models_pb2.Scan(id=scan_id)
        )

    def list_spider_results(self, pagination: models_pb2.Pagination):
        return self.perform_request(self.scanner_stub.ListSpiderResults, pagination)

    def get_spider_result(self, share_id: int):
        return self.perform_request(
            self.scanner_stub.GetSpiderResult,
            scanner_pb2.GetRequest(id=share_id)
        )

    def list_spider_result_filters(self, scan_id: int):
        return self.perform_request(
            self.scanner_stub.ListSpiderResultFilters,
            models_pb2.Scan(id=scan_id)
        )

    def list_shares(self, pagination: models_pb2.Pagination):
        return self.perform_request(self.scanner_stub.ListShares, pagination)

    def get_share(self, share_id: int):
        return self.perform_request(
            self.scanner_stub.GetShare,
            scanner_pb2.GetRequest(id=share_id)
        )

    def list_share_filters(self, scan_id: int):
        return self.perform_request(
            self.scanner_stub.ListShareFilters,
            models_pb2.Scan(id=scan_id)
        )

    def list_share_files(self, pagination: models_pb2.Pagination):
        return self.perform_request(self.scanner_stub.ListShareFiles, pagination)

    def get_share_file(self, share_file_id: int):
        return self.perform_request(
            self.scanner_stub.GetShareFile,
            scanner_pb2.GetRequest(id=share_file_id)
        )

    def list_share_file_filters(self, scan_id: int):
        return self.perform_request(
            self.scanner_stub.ListShareFileFilters,
            models_pb2.Scan(id=scan_id)
        )

    def list_extensions(self, scan_id: int, share_id: int = 0) -> models_pb2.Filter:
        return self.perform_request(
            self.scanner_stub.ListExtensions,
            models_pb2.Share(id=share_id, scan_id=scan_id)
        )

    def index_directory(self, share_file_id: int, max_depth: int = 0, credential_id: int = 0):
        return self.perform_request(
            self.exploit_stub.IndexDirectory,
            exploitation_pb2.IndexRequest(
                share_file_id=share_file_id,
                max_depth=max_depth,
                credential_id=credential_id,
            )
        )

    def download_file(self, share_file_id: int, parse_credentials: bool = False, credential_id: int = 0):
        return self.perform_request(
            self.exploit_stub.DownloadFile,
            exploitation_pb2.DownloadRequest(
                share_file_id=share_file_id,
                parse_credentials=parse_credentials,
                credential_id=credential_id,
            )
        )

    def download_multiple_files(self, share_id: int, parse_credentials: bool, credential_id: int, extension: str = '',
                                max_count: int = 0, skip_downloaded: bool = True, keyword: str = '',
                                share_file_ids: Optional[List[int]] = None, scan_id: int = 0) -> models_pb2.CountMessage:
        return self.perform_request(
            self.exploit_stub.DownloadMultipleFiles,
            exploitation_pb2.MultiDownloadRequest(
                share_id=share_id,
                parse_credentials=parse_credentials,
                credential_id=credential_id,
                extension=extension,
                max_count=max_count,
                skip_downloaded=skip_downloaded,
                keyword=keyword,
                share_file_ids=share_file_ids,
                scan_id=scan_id,
            )
        )

    def parse_files(self, scan_id: int, extension: str = '', max_count: int = 0, skip_parsed: bool = False,
                    keyword: str = '',
                    file_ids: Optional[List[int]] = None) -> models_pb2.CountMessage:
        return self.perform_request(
            self.exploit_stub.ParseFiles,
            exploitation_pb2.MultiParseRequest(
                scan_id=scan_id,
                extension=extension,
                max_count=max_count,
                skip_parsed=skip_parsed,
                keyword=keyword,
                file_ids=file_ids,
            )
        )

    def list_findings(self, pagination: models_pb2.Pagination):
        return self.perform_request(self.scanner_stub.ListFindings, pagination)

    def get_finding(self, finding_id: int):
        return self.perform_request(
            self.scanner_stub.GetFinding,
            scanner_pb2.GetRequest(id=finding_id)
        )

    def list_finding_filters(self, scan_id: int):
        return self.perform_request(
            self.scanner_stub.ListFindingFilters,
            models_pb2.Scan(id=scan_id)
        )

    def export_findings(self, scan_id: int):
        return self.perform_request(
            self.scanner_stub.ExportFindings,
            models_pb2.Scan(id=scan_id)
        )

    def list_credential_sources(self, pagination: models_pb2.Pagination):
        return self.perform_request(
            self.scanner_stub.ListCredentialSources,
            pagination
        )

    def get_credential_source(self, credential_source_id: int):
        return self.perform_request(
            self.scanner_stub.GetCredentialSource,
            scanner_pb2.GetRequest(id=credential_source_id)
        )

    def list_credential_source_filters(self, scan_id: int):
        return self.perform_request(
            self.scanner_stub.ListCredentialSourceFilters,
            models_pb2.Scan(id=scan_id)
        )

    def perform_custom_scan(self, scan_id: int, description: str,
                            nmap_args: str, auto_import: bool):
        return self.perform_request(
            self.scanner_stub.PerformCustomScan,
            models_pb2.CustomScan(
                scan_id=scan_id,
                description=description,
                nmap_args=nmap_args,
                auto_import=auto_import
            )
        )

    def import_custom_scan(self, custom_scan_id: int):
        return self.perform_request(
            self.scanner_stub.ImportCustomScan,
            models_pb2.CustomScan(
                id=custom_scan_id
            )
        )

    def cancel_custom_scan(self, custom_scan_id: int):
        return self.perform_request(
            self.scanner_stub.CancelCustomScan,
            models_pb2.CustomScan(
                id=custom_scan_id
            )
        )

    def list_custom_scans(self, pagination: models_pb2.Pagination):
        return self.perform_request(
            self.scanner_stub.ListCustomScans,
            pagination
        )

    def get_custom_scans(self, custom_scan_id: int):
        return self.perform_request(
            self.scanner_stub.GetCustomScan,
            scanner_pb2.GetRequest(id=custom_scan_id)
        )

    def list_custom_scan_filters(self, scan_id: int):
        return self.perform_request(
            self.scanner_stub.ListCustomScanFilters,
            models_pb2.Scan(id=scan_id)
        )

    def list_access(self, pagination: models_pb2.Pagination):
        return self.perform_request(
            self.scanner_stub.ListAccess,
            pagination
        )

    def get_access(self, access_id: int):
        return self.perform_request(
            self.scanner_stub.GetAccess,
            scanner_pb2.GetRequest(id=access_id)
        )

    def list_access_filters(self, scan_id: int):
        return self.perform_request(
            self.scanner_stub.ListAccessFilters,
            models_pb2.Scan(id=scan_id)
        )

    def check_access(self, credential_id: int, service_id: int, scanner_name: str = ''):
        return self.perform_request(
            self.exploit_stub.CheckAccess,
            exploitation_pb2.AccessRequest(
                credential_id=credential_id,
                service_id=service_id,
                scanner_name=scanner_name,
            )
        )

    def check_multiple_access(self, credential_id: int, scan_id: int, max_check: int = 0,
                              scanner_name: str = '', port: int = 0, domain_id: int = 0,
                              skip_checked: bool = False):
        return self.perform_request(
            self.exploit_stub.CheckMultipleAccess,
            exploitation_pb2.AccessRequest(
                credential_id=credential_id,
                scan_id=scan_id,
                max_check=max_check,
                scanner_name=scanner_name,
                port=port,
                domain_id=domain_id,
                skip_checked=skip_checked,
            )
        )

    def create_password_spray(self, scan_id: int, service_id: int, domain_id: int = 0,
                              password_policy_id: int = 0, credential_id: int = 0, delay_seconds: int = 0,
                              worker_count: int = 0, stop_on_locked: bool = False, check_counter: bool = False,
                              skip_users_with_credentials: bool = True, usernames: Optional[List[str]] = None,
                              user_ids: Optional[List[int]] = None, passwords: Optional[List[str]] = None,
                              max_total_attempts: int = 0, max_attempts_run: int = 0, login_scanner: str = '',
                              load_domain_users: bool = False):
        password_spray = models_pb2.PasswordSpray(
            scan_id=scan_id,
            service_id=service_id,
            domain_id=domain_id,
            password_policy_id=password_policy_id,
            credential_id=credential_id,
            delay_seconds=delay_seconds,
            worker_count=worker_count,
            stop_on_locked=stop_on_locked,
            check_counter=check_counter,
            skip_users_with_credentials=skip_users_with_credentials,
            max_total_attempts=max_total_attempts,
            max_attempts_run=max_attempts_run,
            login_scanner=login_scanner,
            passwords=passwords,
            load_domain_users=load_domain_users
        )

        if usernames:
            for user in usernames:
                user_pb2 = password_spray.users.add()
                user_pb2.user.MergeFrom(models_pb2.User(username=user))

        if user_ids:
            for user_id in user_ids:
                user_pb2 = password_spray.users.add()
                user_pb2.user.MergeFrom(models_pb2.User(id=user_id))

        return self.perform_request(
            self.exploit_stub.CreatePasswordSpray,
            password_spray
        )

    def start_password_spray(self, password_spray_id: int):
        return self.perform_request(
            self.exploit_stub.StartPasswordSpray,
            models_pb2.PasswordSpray(id=password_spray_id)
        )

    def cancel_password_spray(self, password_spray_id: int):
        return self.perform_request(
            self.exploit_stub.CancelPasswordSpray,
            models_pb2.PasswordSpray(id=password_spray_id)
        )

    def add_password_spray_user(self, password_spray_id: int, user_id: int = 0, username: str = ''):
        user = models_pb2.PasswordSprayUser(password_spray_id=password_spray_id, user_id = user_id)
        if username:
            user.user.MergeFrom(models_pb2.User(username=username))
        return self.perform_request(
            self.exploit_stub.AddPasswordSprayUser,
            user
        )

    def delete_password_spray_user(self, password_spray_user_id: int):
        return self.perform_request(
            self.exploit_stub.DeletePasswordSprayUser,
            models_pb2.PasswordSprayUser(
                id=password_spray_user_id
            )
        )

    def add_password_spray_run(self, password_spray_id: int, password: str):
        return self.perform_request(
            self.exploit_stub.AddPasswordSprayRun,
            models_pb2.PasswordSprayRun(
                password_spray_id=password_spray_id,
                password=password
            )
        )

    def delete_password_spray_run(self, password_spray_run_id: int):
        return self.perform_request(
            self.exploit_stub.DeletePasswordSprayRun,
            models_pb2.PasswordSprayRun(
                id=password_spray_run_id
            )
        )

    def list_password_spray_filters(self, scan_id: int):
        return self.perform_request(
            self.scanner_stub.ListPasswordSprayFilters,
            models_pb2.Scan(id=scan_id)
        )

    def list_password_sprays(self, pagination: models_pb2.Pagination):
        return self.perform_request(
            self.scanner_stub.ListPasswordSprays,
            pagination
        )

    def get_password_spray(self, spray_id: int):
        return self.perform_request(
            self.scanner_stub.GetPasswordSpray,
            scanner_pb2.GetRequest(id=spray_id)
        )

    def list_password_spray_runs(self, pagination: models_pb2.Pagination):
        return self.perform_request(
            self.scanner_stub.ListPasswordSprayRuns,
            pagination
        )

    def list_password_spray_run_filters(self, scan_id: int):
        return self.perform_request(
            self.scanner_stub.ListPasswordSprayRunFilters,
            models_pb2.Pagination(id=scan_id)
        )

    def list_password_spray_users(self, pagination: models_pb2.Pagination):
        return self.perform_request(
            self.scanner_stub.ListPasswordSprayUsers,
            pagination
        )

    def list_password_spray_user_filters(self, scan_id: int):
        return self.perform_request(
            self.scanner_stub.ListPasswordSprayUserFilters,
            models_pb2.Pagination(id=scan_id)
        )

    # Bloodhound methods
    def find_local_admins_for_group(self, scan_id: int, group_id: int):
        return self.perform_request(
            self.bloodhound_stub.LocalAdminsForGroup,
            bloodhound_pb2.BloodHoundRequest(
                scan_id=scan_id,
                group_id=group_id
            )
        )

    def find_local_admins_for_user(self, scan_id: int, user_id: int):
        return self.perform_request(
            self.bloodhound_stub.LocalAdminsForUser,
            bloodhound_pb2.BloodHoundRequest(
                scan_id=scan_id,
                user_id=user_id
            )
        )

    def run_bloodhound(self, scan_id: int, domain_id: int, credential_id: int, collection_methods: List[str]):
        return self.perform_request(
            self.bloodhound_stub.RunBloodHound,
            bloodhound_pb2.BloodHoundRequest(
                scan_id=scan_id,
                domain_id=domain_id,
                credential_id=credential_id,
                collection_methods=collection_methods,
            )
        )

    def list_bloodhound_runs(self, pagination: models_pb2.Pagination):
        return self.perform_request(
            self.bloodhound_stub.ListBloodHoundRuns,
            pagination
        )

    def get_bloodhound_run(self, bloodhound_run_id: int):
        return self.perform_request(
            self.bloodhound_stub.GetBloodHoundRun,
            scanner_pb2.GetRequest(id=bloodhound_run_id)
        )

    def list_collection_methods(self):
        return self.perform_request(
            self.bloodhound_stub.ListBloodHoundCollectionMethods,
            models_pb2.EmptyRequest()
        )

    # metasploit functions

    def list_metasploit_consoles(self):
        return self.perform_request(
            self.metasploit_stub.ListConsoles,
            models_pb2.EmptyRequest()
        )

    def get_metasploit_console(self, id):
        return self.perform_request(
            self.metasploit_stub.GetConsole,
            metasploit_pb2.Console(
                id=id
            )
        )

    def create_metasploit_console(self):
        return self.perform_request(
            self.metasploit_stub.CreateConsole,
            models_pb2.EmptyRequest()
        )

    def stop_metasploit_console(self, cid: str):
        return self.perform_request(
            self.metasploit_stub.StopConsole,
            metasploit_pb2.Console(
                id=cid
            )
        )

    def write_to_console(self, cid: str, message: str):
        return self.perform_request(
            self.metasploit_stub.WriteToConsole,
            metasploit_pb2.ConsoleMessage(
                id=cid,
                message=message,
            )
        )

    def list_metasploit_sessions(self):
        return self.perform_request(
            self.metasploit_stub.ListSessions,
            models_pb2.EmptyRequest()
        )

    def get_metasploit_session(self, id: str):
        return self.perform_request(
            self.metasploit_stub.GetSession,
            metasploit_pb2.MetasploitSession(id=id)
        )

    def write_to_session(self, sid: str, message: str):
        return self.perform_request(
            self.metasploit_stub.WriteToSession,
            metasploit_pb2.ConsoleMessage(
                id=sid,
                message=message
            )
        )

    def calc_ranges(self, scan_id: int, prefix: int):
        return self.perform_request(
            self.scanner_stub.CalcRanges,
            scanner_pb2.Prefix(
                scan_id=scan_id,
                prefix=prefix
            )
        )

    # Terminal related calls
    def list_terminals(self):
        return self.perform_request(
            self.terminal_stub.ListTerminals,
            models_pb2.EmptyRequest()
        )

    def get_terminal(self, terminal_id: int):
        return self.perform_request(
            self.terminal_stub.GetTerminal,
            terminal_pb2.Terminal(
                id=terminal_id
            )
        )

    def new_terminal(self):
        return self.perform_request(
            self.terminal_stub.NewTerminal,
            models_pb2.EmptyRequest()
        )

    def terminal_send_input(self, terminal_id: int, input_bytes: bytes):
        return self.perform_request(
            self.terminal_stub.SendInput,
            terminal_pb2.TerminalInput(
                id=terminal_id,
                input=input_bytes,
            )
        )

    def stop_terminal(self, terminal_id: int):
        return self.perform_request(
            self.terminal_stub.StopTerminal,
            terminal_pb2.Terminal(
                id=terminal_id
            )
        )

    def update_terminal(self, terminal_id: int, label: str):
        """Update the label of the terminal"""
        return self.perform_request(
            self.terminal_stub.UpdateTerminal,
            terminal_pb2.Terminal(
                id=terminal_id,
                label=label
            )
        )

    def resize_terminal(self, terminal_id: int, rows: int, cols: int):
        """Resize the terminal to the given rows and cols"""
        size = terminal_pb2.TerminalSize(
            rows=rows,
            cols=cols,
        )
        return self.perform_request(
            self.terminal_stub.ResizeTerminal,
            terminal_pb2.Terminal(
                id=terminal_id,
                size=size
            )
        )


class CallbackClient(Client):
    """
        CallbackClient implements functions to report results to a server.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback_stub = callback_pb2_grpc.CallbackServiceStub(self.channel)

    def reset_stubs(self):
        """Reset the stub"""
        self.callback_stub = callback_pb2_grpc.CallbackServiceStub(self.channel)

    def new_host(self, host_id: int, scan_id: int, domain_id: int) -> None:
        self.perform_request(
            self.callback_stub.NewHost,
            callback_pb2.Callback(
                host_id=host_id,
                scan_id=scan_id,
                domain_id=domain_id
            )
        )

    def new_service(self, service_id: int, scan_id: int, host_id: int, port: int, domain_id: int) -> None:
        self.perform_request(
            self.callback_stub.NewService,
            callback_pb2.Callback(
                service_id=service_id,
                scan_id=scan_id,
                host_id=host_id,
                port=port,
                domain_id=domain_id,
            )
        )

    def new_vulnerability(self, vuln_id: int, scan_id: int, service_id: int,
                          exploit_ids: List[str], port: int, host_id: int, domain_id: int) -> None:
        self.perform_request(
            self.callback_stub.NewService,
            callback_pb2.Callback(
                vuln_id=vuln_id,
                scan_id=scan_id,
                service_id=service_id,
                exploit_ids=exploit_ids,
                port=port,
                host_id=host_id,
                domain_id=domain_id,
            )
        )

    def new_user(self, user_id: int, scan_id: int) -> None:
        self.perform_request(
            self.callback_stub.NewService,
            callback_pb2.Callback(
                user_id=user_id,
                scan_id=scan_id,
            )
        )

    def new_credential(self, credential_id: int, scan_id: int, domain_id: int) -> None:
        self.perform_request(
            self.callback_stub.NewService,
            callback_pb2.Callback(
                credential_id=credential_id,
                scan_id=scan_id,
                domain_id=domain_id,
            )
        )

    def new_domain(self, scan_id: int, domain_id: int) -> None:
        self.perform_request(
            self.callback_stub.NewService,
            callback_pb2.Callback(
                domain_id=domain_id,
                scan_id=scan_id,
            )
        )

    def console_output(self, cid: str, output: str, prompt: str) -> None:
        """Report console output to the server"""
        self.perform_request(
            self.callback_stub.NewConsoleOutput,
            metasploit_pb2.ConsoleOutput(
                cid=cid,
                output=output,
                prompt=prompt,
            )
        )

    def session_output(self, sid: str, message: str) -> None:
        """Report session message to the server"""
        self.perform_request(
            self.callback_stub.NewSessionOutput,
            metasploit_pb2.SessionOutput(
                sid=sid,
                message=message,
            )
        )

    def terminal_output(self, terminal_id: int, output_bytes: bytes) -> None:
        """Report terminal output to the server"""
        self.perform_request(
            self.callback_stub.NewTerminalOutput,
            terminal_pb2.TerminalOutput(
                id=terminal_id,
                output=output_bytes,
            )
        )

    def report_statistics(self, scan_id: int, hosts: int = 0, services: int = 0, credentials: int = 0,
                          exploits: Optional[List[Tuple[str, int]]] = None,
                          vulnerabilities: Optional[List[Tuple[str, int]]] = None,
                          passwords: Optional[List[Tuple[str, int]]] = None,
                          loot: Optional[List[Tuple[str, int]]] = None) -> None:
        """Report the statistics to the server"""
        result = callback_pb2.StatisticsMessage(
            hosts=hosts, services=services, credentials=credentials, scan_id=scan_id
        )
        if exploits:
            for key, value in exploits:
                message_pb2 = result.exploits.add()
                message_pb2.name = key
                message_pb2.count = value

        if vulnerabilities:
            for key, value in vulnerabilities:
                message_pb2 = result.vulnerabilities.add()
                message_pb2.name = key
                message_pb2.count = value

        if passwords:
            for key, value in passwords:
                message_pb2 = result.passwords.add()
                message_pb2.name = key
                message_pb2.count = value

        if loot:
            for key, value in loot:
                message_pb2 = result.loot.add()
                message_pb2.name = key
                message_pb2.count = value

        self.perform_request(
            self.callback_stub.ReportStatistics,
            result
        )


class WireguardClient(Client):
    """
        Client to communicate with the wireguard grpc server.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wireguard_stub = wireguard_pb2_grpc.WireguardStub(self.channel)

    def generate_key(self):
        """Generate a public / private key combination"""
        return self.perform_request(
            self.wireguard_stub.GenKey,
            models_pb2.EmptyMessage()
        )

    def add_peer(self, public_key: str, allowed_ips: List[str]):
        """Add a peer to the server"""
        peer = wireguard_pb2.Peer(
            public_key=public_key,
            allowed_ips=[wireguard_pb2.IP(ip=ip) for ip in allowed_ips]
        )
        return self.perform_request(
            self.wireguard_stub.AddPeer,
            peer
        )

    def remove_peer(self, public_key: str):
        """Remove a peer from the server"""
        peer = wireguard_pb2.Peer(
            public_key=public_key
        )
        return self.perform_request(
            self.wireguard_stub.RemovePeer,
            peer
        )

    def list_peers(self):
        """List the current peers of the server"""
        return self.perform_request(
            self.wireguard_stub.ListPeers,
            models_pb2.EmptyRequest()
        )

    def get_interface(self):
        """Get the interface of the server"""
        return self.perform_request(
            self.wireguard_stub.GetInterface,
            models_pb2.EmptyRequest()
        )


class CrackerClient(Client):
    """The CrackerClient is used to connect to a password cracking server."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cracker_stub = cracker_pb2_grpc.CrackingServiceStub(self.channel)

    def reset_stubs(self):
        """Reset the stub"""
        self.cracker_stub = cracker_pb2_grpc.CrackingServiceStub(self.channel)

    def ping(self, message: str = 'ping'):
        """Ping the services, will ping back the message"""
        return self.perform_request(
            self.cracker_stub.Ping,
            cracker_pb2.PingMessage(message=message)
        )

    def get_list(self):
        """Will return the wordlists and the rules lists"""
        return self.perform_request(
            self.cracker_stub.GetLists,
            cracker_pb2.EmptyMessage()
        )

    @staticmethod
    def create_task_message(rules: str = '', wordlist: str = '', mask: str = '') -> cracker_pb2.Task:
        """Return a Task protobuf message from the given arguments."""
        return cracker_pb2.Task(
            rules=rules,
            wordlist=wordlist,
            mask=mask
        )

    def add_job(self, hashcat_id: int, tasks: List[cracker_pb2.Task], priority: int = 0):
        """Add a new job"""
        message = cracker_pb2.Job(
            hashcat_id=hashcat_id,
            priority=priority,
        )

        for task in tasks:
            task_pb2 = message.tasks.add()
            task_pb2.MergeFrom(task)

        return self.perform_request(
            self.cracker_stub.AddJob,
            message
        )

    def stream_hashes(self, job_id: int, stream: TextIO):
        """Stream the hashes from the stream to the cracker for the given job_id"""
        def hash_iterator():
            for line in stream.readlines():
                line = line.strip()
                yield cracker_pb2.Hash(hash=line, id=job_id)

        return self.perform_request(
            self.cracker_stub.AddHashes,
            hash_iterator()
        )

    def start_job(self, job_id: int):
        """Start the given job"""
        return self.perform_request(
            self.cracker_stub.StartJob,
            cracker_pb2.Job(id=job_id)
        )

    def list_jobs(self, start: int, count: int):
        """List the jobs from the start to the count."""
        return self.perform_request(
            self.cracker_stub.ListJobs,
            cracker_pb2.JobPagination(
                start=start,
                count=count,
            )
        )

    def get_job(self, job_id: int):
        """Get the job with the given job_id"""
        return self.perform_request(
            self.cracker_stub.GetJob,
            cracker_pb2.Job(
                id=job_id
            )
        )

    def get_results(self, job_id: int):
        """Will return a stream of the result hashes that were cracked."""
        job = cracker_pb2.Job(id=job_id)
        for entry in self.cracker_stub.GetResults(job):
            yield entry

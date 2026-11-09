// METADATA
// version: 0.4.0
// description: Contrato reescrito

//SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

interface Recovered_Smart_Contract {
    function get_contract_data(
            ) external view returns(address[] memory ,
                                    address[] memory,
                                    Smart_Contract_Prototype.User[] memory,
                                    address[] memory,
                                    Smart_Contract_Prototype.Ornamental_block[] memory);
}

contract Smart_Contract_Prototype {
    address immutable public ADMINISTRATOR;

    struct Metadata {
        address uid;
        uint list_index;
        string registration_timestamp;
        string last_update_timestamp;
    }

    struct User {
        Metadata metadata;
        string name;
        string cnpj;
        string email_address;
        address[] ornamental_blocks_list;
    }

    struct Ornamental_block {
        Metadata metadata;
        string mining_data; // company: , mining site: , mining date:
        string code;
        string properties; // material: , dimensions in mm: , weight in kg:
        string hash;
        bool is_active;
        address[] last_owners_list;
        string[] invoice_number_list;
    }

    mapping(address => User) private users_map;
    address[] private _user_uids_list;

    mapping(address => Ornamental_block) private ornamental_blocks_map;
    address[] private _ornamental_block_uids_list;

    address[] private recovered_contracts_address_list;
    string private _last_updated_timestamp;

    constructor(address contract_to_recover_address){
        ADMINISTRATOR = msg.sender;
        if (contract_to_recover_address != address(0)) {
            recover_data_from_previous_contract(contract_to_recover_address);
        } else {
            add_new_user(address(0),
                         "",
                         "",
                         "",
                         "");
        }
        recovered_contracts_address_list.push(address(this));
        _last_updated_timestamp = "contract deploy";
    }

    // Busca os dados dos usuários e dos blocos ornamentais já registrados em um contrato passado (usada no backup) - TX FROM CONTRACT ITSELF
    function recover_data_from_previous_contract(address contract_to_recover_address)
        private {

        require(msg.sender == ADMINISTRATOR);

        User[] memory recovered_users_map;
        Ornamental_block[] memory recovered_ornamental_blocks_map;
        (recovered_contracts_address_list, _user_uids_list, recovered_users_map, _ornamental_block_uids_list, recovered_ornamental_blocks_map) = Recovered_Smart_Contract(contract_to_recover_address).get_contract_data();

        uint previous_number_of_users = _user_uids_list.length;
        if (previous_number_of_users > 0) {

            for(uint index = 0; index < previous_number_of_users; index++) {
                users_map[_user_uids_list[index]] = recovered_users_map[index];
            }
        }
        uint previous_number_of_ornamental_blocks = _ornamental_block_uids_list.length;
        if (previous_number_of_ornamental_blocks > 0) {

            for(uint index = 0; index < previous_number_of_ornamental_blocks; index++) {
                ornamental_blocks_map[_ornamental_block_uids_list[index]] = recovered_ornamental_blocks_map[index];
            }
        }
    }

    // Retorna os dados de usuários e blocos ornamentais para um contrato atualizado - CALL FROM OTHER CONTRACT
    function get_contract_data()
        external view returns(address[] memory recovered_contractss_address_list,
                              address[] memory users_uids_list,
                              User[] memory users_list,
                              address[] memory ornamental_blocks_uids_list,
                              Ornamental_block[] memory ornamental_blocks_list) {

        users_list = new User[](_user_uids_list.length);

        for(uint index = 0; index < _user_uids_list.length; index++) {

            users_list[index] = (users_map[_user_uids_list[index]]);
        }

        ornamental_blocks_list = new Ornamental_block[](_ornamental_block_uids_list.length);

        for(uint index = 0; index < _ornamental_block_uids_list.length; index++) {

            ornamental_blocks_list[index] = (ornamental_blocks_map[_ornamental_block_uids_list[index]]);
        }

        return (recovered_contracts_address_list, _user_uids_list, users_list, _ornamental_block_uids_list, ornamental_blocks_list);
    }

    // Retorna o último carimbo de data e hora atualizado - CALL FROM USER
    function get_last_updated_timestamp() public view returns(string memory last_updated_timestamp) {

        return _last_updated_timestamp;
    }

    // Retorna lista de uids dos usuários - CALL FROM USER
    function get_user_uids_list()
        public view returns(address[] memory user_uids_list) {

        return _user_uids_list;
    }

    // Retorna lista de uids dos blocos ornamentais - CALL FROM USER
    function get_ornamental_block_uids_list()
        public view returns(address[] memory ornamental_block_uids_list) {

        return _ornamental_block_uids_list;
    }

    // Retorna true se o endereço inserido já pertencer à um usuário - CALL FROM USER
    function is_user(address user_uid)
        public view returns(bool user_found) {

        if(_user_uids_list.length == 0) return false;

        return user_found = (users_map[user_uid].metadata.uid == user_uid);
    }

    // Retorna true se o endereço inserido já pertencer à um bloco ornamental - CALL FROM USER
    function is_ornamental_block(address ornamental_block_uid)
        public view returns(bool ornamental_block_found) {

        if(_ornamental_block_uids_list.length == 0) return false;

        return ornamental_block_found = (ornamental_blocks_map[ornamental_block_uid].metadata.uid == ornamental_block_uid);
    }

    // Retorna true se o endereço inserido já pertencer à um bloco ornamental - CALL FROM USER
    function is_ornamental_block_active(address ornamental_block_uid)
        public view returns(bool ornamental_block_is_active) {

        require(_ornamental_block_uids_list.length > 0);
        require(is_ornamental_block(ornamental_block_uid));

        return ornamental_blocks_map[ornamental_block_uid].is_active;
    }

    // Adiciona um novo usuário ao contrato - TX FROM USER
    function add_new_user(address user_uid,
                          string memory user_name,
                          string memory user_cnpj,
                          string memory user_email_address,
                          string memory timestamp)
        public {

        require(msg.sender == ADMINISTRATOR);
        require(!is_user(user_uid), "User already exists!");

        address u_uid = user_uid;
        users_map[u_uid].metadata.uid = user_uid;
        users_map[u_uid].metadata.list_index = _user_uids_list.length;
        users_map[u_uid].metadata.registration_timestamp = timestamp;
        users_map[u_uid].metadata.last_update_timestamp = timestamp;
        users_map[u_uid].name = user_name;
        users_map[u_uid].cnpj = user_cnpj;
        users_map[u_uid].email_address = user_email_address;

        _user_uids_list.push(u_uid);
        _last_updated_timestamp = timestamp;
    }

    // Adiciona até 5 novos usuários ao contrato - TX FROM USER
    function add_up_to_5_new_users(address[5] memory user_uid_list,
                                   string[5] memory user_name_list,
                                   string[5] memory user_cnpj_list,
                                   string[5] memory user_email_address_list,
                                   string memory timestamp)
        external {

        require(msg.sender == ADMINISTRATOR);

        for (uint index = 0; index < 5; index++) {
            if(user_uid_list[index] == address(0)) break;
            add_new_user(user_uid_list[index],
                         user_name_list[index],
                         user_cnpj_list[index],
                         user_email_address_list[index],
                         timestamp);
        }
    }

    // Adiciona até 20 novos usuários ao contrato - TX FROM USER
    function add_up_to_20_new_users(address[20] memory user_uid_list,
                                    string[20] memory user_name_list,
                                    string[20] memory user_cnpj_list,
                                    string[20] memory user_email_address_list,
                                    string memory timestamp)
        external {

        require(msg.sender == ADMINISTRATOR);

        for (uint index = 0; index < 20; index++) {
            if(user_uid_list[index] == address(0)) break;
            add_new_user(user_uid_list[index],
                         user_name_list[index],
                         user_cnpj_list[index],
                         user_email_address_list[index],
                         timestamp);
        }
    }

    // Adiciona um novo bloco ornamental ao contrato - TX FROM USER
    function add_new_ornamental_block(address ornamental_block_uid,
                                      string memory mining_data,
                                      string memory code,
                                      string memory properties,
                                      string memory hash,
                                      address owners_uid,
                                      string memory timestamp)
        public {

        require(msg.sender == ADMINISTRATOR);
        require(!is_ornamental_block(ornamental_block_uid), "Ornamental block address already exists!");

        address ob_uid = ornamental_block_uid;
        ornamental_blocks_map[ob_uid].metadata.uid = ornamental_block_uid;
        ornamental_blocks_map[ob_uid].metadata.list_index = _ornamental_block_uids_list.length;
        ornamental_blocks_map[ob_uid].metadata.registration_timestamp = timestamp;
        ornamental_blocks_map[ob_uid].metadata.last_update_timestamp = timestamp;
        ornamental_blocks_map[ob_uid].mining_data = mining_data;
        ornamental_blocks_map[ob_uid].code = code;
        ornamental_blocks_map[ob_uid].properties = properties;
        ornamental_blocks_map[ob_uid].hash = hash;
        ornamental_blocks_map[ob_uid].is_active = true;
        ornamental_blocks_map[ob_uid].last_owners_list.push(owners_uid);
        _ornamental_block_uids_list.push(ob_uid);

        users_map[owners_uid].ornamental_blocks_list.push(ob_uid);
        users_map[owners_uid].metadata.last_update_timestamp = timestamp;
        _last_updated_timestamp = timestamp;
    }

    // Adiciona até 5 novos blocos ornamentais ao contrato - TX FROM USER
    function add_up_to_5_new_ornamental_blocks(address[5] memory ornamental_block_uid_list,
                                               string[5] memory mining_data_list,
                                               string[5] memory code_list,
                                               string[5] memory properties_list,
                                               string[5] memory hash_list,
                                               address[5] memory owners_uid_list,
                                               string memory timestamp)
        external {

        require(msg.sender == ADMINISTRATOR);

        for (uint index = 0; index < 5; index++) {
            if(ornamental_block_uid_list[index] == address(0)) break;
            add_new_ornamental_block(ornamental_block_uid_list[index],
                           mining_data_list[index],
                           code_list[index],
                           properties_list[index],
                           hash_list[index],
                           owners_uid_list[index],
                           timestamp);
        }
    }

    // Adiciona até 20 novos blocos ornamentais ao contrato - TX FROM USER
    function add_up_to_20_new_ornamental_blocks(address[20] memory ornamental_block_uid_list,
                                                string[20] memory mining_data_list,
                                                string[20] memory code_list,
                                                string[20] memory properties_list,
                                                string[20] memory hash_list,
                                                address[20] memory owners_uid_list,
                                                string memory timestamp)
        external {

        require(msg.sender == ADMINISTRATOR);

        for (uint index = 0; index < 20; index++) {
            if(ornamental_block_uid_list[index] == address(0)) break;
            add_new_ornamental_block(ornamental_block_uid_list[index],
                           mining_data_list[index],
                           code_list[index],
                           properties_list[index],
                           hash_list[index],
                           owners_uid_list[index],
                           timestamp);
        }
    }

    // Desativa e transfere um bloco ornamental para o usuário nulo - TX FROM USER
    function deactivate_ornamental_block(address ornamental_block_uid,
                                         string memory timestamp)
        public {

        require(msg.sender == ADMINISTRATOR);

        transfer_ornamental_block(ornamental_block_uid,
                                  _user_uids_list[0],
                                  "",
                                  timestamp);
        ornamental_blocks_map[ornamental_block_uid].is_active = false;
        _last_updated_timestamp = timestamp;
    }

    // Desativa e transfere até 5 blocos ornamentais para o usuário nulo - TX FROM USER
    function deactivate_up_to_5_ornamental_blocks(address[5] memory ornamental_block_uid_list,
                                                  string memory timestamp)
        external {

        require(msg.sender == ADMINISTRATOR);

        for (uint index = 0; index < 5; index++) {
            if(ornamental_block_uid_list[index] == address(0)) break;
            deactivate_ornamental_block(ornamental_block_uid_list[index],
                                        timestamp);
        }
    }

    // Desativa e transfere até 20 blocos ornamentais para o usuário nulo - TX FROM USER
    function deactivate_up_to_20_ornamental_blocks(address[20] memory ornamental_block_uid_list,
                                                   string memory timestamp)
        external {

        require(msg.sender == ADMINISTRATOR);

        for (uint index = 0; index < 20; index++) {
            if(ornamental_block_uid_list[index] == address(0)) break;
            deactivate_ornamental_block(ornamental_block_uid_list[index],
                                        timestamp);
        }
    }

    // Retorna as informações de um usuário pelo seu endereço - CALL FROM USER
    function get_user_data(address user_uid)
        external view returns(address user_uid_,
                              uint user_list_index,
                              string memory user_registration_timestamp,
                              string memory user_last_update_timestamp,
                              string memory user_name,
                              string memory user_cnpj,
                              string memory user_email_address,
                              address[] memory ornamental_blocks_list) {

        require(is_user(user_uid), "User not found!");

        address u_uid = user_uid;
        user_uid_ = user_uid;
        user_list_index = users_map[u_uid].metadata.list_index;
        user_registration_timestamp = users_map[u_uid].metadata.registration_timestamp;
        user_last_update_timestamp = users_map[u_uid].metadata.last_update_timestamp;
        user_name = users_map[u_uid].name;
        user_cnpj = users_map[u_uid].cnpj;
        user_email_address = users_map[u_uid].email_address;
        ornamental_blocks_list = users_map[u_uid].ornamental_blocks_list;
    }

    // Retorna as informações de um usuário pelo seu endereço - CALL FROM USER
    function get_ornamental_block_data(address ornamental_block_uid)
        external view returns(address ornamental_block_uid_,
                              uint ornamental_block_list_index,
                              string memory ornamental_block_registration_timestamp,
                              string memory ornamental_block_last_update_timestamp,
                              string memory ornamental_block_mining_data,
                              string memory ornamental_block_code,
                              string memory ornamental_block_properties,
                              string memory ornamental_block_hash,
                              bool ornamental_block_is_active,
                              address[] memory ornamental_block_last_owners,
                              string[] memory ornamental_block_invoice_numbers) {

        require(is_ornamental_block(ornamental_block_uid), "Ornamental block not found!");

        address ob_uid = ornamental_block_uid;
        ornamental_block_uid_ = ornamental_block_uid;
        ornamental_block_list_index = ornamental_blocks_map[ob_uid].metadata.list_index;
        ornamental_block_registration_timestamp = ornamental_blocks_map[ob_uid].metadata.registration_timestamp;
        ornamental_block_last_update_timestamp = ornamental_blocks_map[ob_uid].metadata.last_update_timestamp;
        ornamental_block_mining_data = ornamental_blocks_map[ob_uid].mining_data;
        ornamental_block_code = ornamental_blocks_map[ob_uid].code;
        ornamental_block_properties = ornamental_blocks_map[ob_uid].properties;
        ornamental_block_hash = ornamental_blocks_map[ob_uid].hash;
        ornamental_block_is_active = ornamental_blocks_map[ob_uid].is_active;
        ornamental_block_last_owners = ornamental_blocks_map[ob_uid].last_owners_list;
        ornamental_block_invoice_numbers = ornamental_blocks_map[ob_uid].invoice_number_list;
    }

    // Transfere um bloco para outro usuário - TX FROM USER
    function transfer_ornamental_block(address ornamental_block_uid,
                                       address new_owner_uid,
                                       string memory invoice_number,
                                       string memory timestamp)
        public {

        require(msg.sender == ADMINISTRATOR);

        require(is_user(new_owner_uid), "User not found!");
        require(is_ornamental_block(ornamental_block_uid), "Ornamental block not found!");

        address old_owner_uid = ornamental_blocks_map[ornamental_block_uid].last_owners_list[ornamental_blocks_map[ornamental_block_uid].last_owners_list.length - 1];

        require(old_owner_uid != new_owner_uid, "User receiver already has this ornamental block!");

        uint new_length = users_map[old_owner_uid].ornamental_blocks_list.length - 1;
        address[] memory new_list = new address[](new_length);
        uint count = 0;

        for (uint index = 0; index <= new_length; index++) {

            if (users_map[old_owner_uid].ornamental_blocks_list[index] != ornamental_block_uid) {

                new_list[count] = users_map[old_owner_uid].ornamental_blocks_list[index];
                count++;
            }
        }
        ornamental_blocks_map[ornamental_block_uid].metadata.last_update_timestamp = timestamp;
        ornamental_blocks_map[ornamental_block_uid].last_owners_list.push(new_owner_uid);
        ornamental_blocks_map[ornamental_block_uid].invoice_number_list.push(invoice_number);

        users_map[old_owner_uid].metadata.last_update_timestamp = timestamp;
        users_map[old_owner_uid].ornamental_blocks_list = new_list;

        users_map[new_owner_uid].metadata.last_update_timestamp = timestamp;
        users_map[new_owner_uid].ornamental_blocks_list.push(ornamental_block_uid);
        _last_updated_timestamp = timestamp;
    }

    // Transfere até 5 blocos para 5 usuários - TX FROM USER
    function transfer_up_to_5_ornamental_blocks(address[5] memory ornamental_block_uid_list,
                                                address[5] memory new_owner_uid_list,
                                                string[5] memory invoice_number_list,
                                                string memory timestamp)
        external {

        require(msg.sender == ADMINISTRATOR);

        for (uint index = 0; index < 5; index++) {
            if(ornamental_block_uid_list[index] == address(0)) break;
            transfer_ornamental_block(ornamental_block_uid_list[index],
                                      new_owner_uid_list[index],
                                      invoice_number_list[index],
                                      timestamp);
        }
    }

    // Transfere até 20 blocos para 10 usuários - TX FROM USER
    function transfer_up_to_20_ornamental_blocks(address[20] memory ornamental_block_uid_list,
                                                 address[20] memory new_owner_uid_list,
                                                 string[20] memory invoice_number_list,
                                                 string memory timestamp)
        external {

        require(msg.sender == ADMINISTRATOR);

        for (uint index = 0; index < 20; index++) {
            if(ornamental_block_uid_list[index] == address(0)) break;
            transfer_ornamental_block(ornamental_block_uid_list[index],
                                      new_owner_uid_list[index],
                                      invoice_number_list[index],
                                      timestamp);
        }
    }
}
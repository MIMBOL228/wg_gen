prk=`wg genkey` && pbk=`echo $prk | wg pubkey` && printf "$prk $pbk"
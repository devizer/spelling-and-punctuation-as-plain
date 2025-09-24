function title() { echo -n -e "\033]0;$1\007"; echo ""; echo ""; Say "$1"; }
counter=0;
total=69
function run1dump() {
  counter=$((counter+1))
  local aff="/usr/share/hunspell/$1"
  local dic="/usr/share/hunspell/$2"
  local lang="$3"
  local output="$lang.txt"
  title "$counter of $total: DUMP Words for $lang"
  python3 hunspell_dump_forms_v12.py \
      --aff "$aff" \
      --dic "$dic" \
      --lang "$lang" \
      --output "$output" \
      --stream --removed-log "$output.removed_zero_lines.txt"
}
# source ~/hunspell_env/bin/activate
run1dump en_US.aff en_US.dic en_US en_US.txt
run1dump ru_RU.aff ru_RU.dic ru_RU ru_RU.txt
run1dump uk_UA.aff uk_UA.dic uk_UA uk_UA.txt

# Remaining hunspell languages
run1dump af_ZA.aff af_ZA.dic af_ZA
run1dump an_ES.aff an_ES.dic an_ES
run1dump ar.aff ar.dic ar
run1dump ar_AE.aff ar_AE.dic ar_AE
run1dump ar_BH.aff ar_BH.dic ar_BH
run1dump ar_DZ.aff ar_DZ.dic ar_DZ
run1dump ar_EG.aff ar_EG.dic ar_EG
run1dump ar_IQ.aff ar_IQ.dic ar_IQ
run1dump ar_JO.aff ar_JO.dic ar_JO
run1dump ar_KW.aff ar_KW.dic ar_KW
run1dump ar_LB.aff ar_LB.dic ar_LB
run1dump ar_LY.aff ar_LY.dic ar_LY
run1dump ar_MA.aff ar_MA.dic ar_MA
run1dump ar_OM.aff ar_OM.dic ar_OM
run1dump ar_QA.aff ar_QA.dic ar_QA
run1dump ar_SA.aff ar_SA.dic ar_SA
run1dump ar_SD.aff ar_SD.dic ar_SD
run1dump ar_SY.aff ar_SY.dic ar_SY
run1dump ar_TN.aff ar_TN.dic ar_TN
run1dump ar_YE.aff ar_YE.dic ar_YE
run1dump be_BY.aff be_BY.dic be_BY
run1dump bg_BG.aff bg_BG.dic bg_BG
run1dump bn_BD.aff bn_BD.dic bn_BD
run1dump bn_IN.aff bn_IN.dic bn_IN
run1dump bo.aff bo.dic bo
run1dump bo_CN.aff bo_CN.dic bo_CN
run1dump bo_IN.aff bo_IN.dic bo_IN
run1dump br_FR.aff br_FR.dic br_FR
run1dump bs_BA.aff bs_BA.dic bs_BA
run1dump ca.aff ca.dic ca
run1dump ca_ES.aff ca_ES.dic ca_ES
run1dump ca_ES-valencia.aff ca_ES-valencia.dic ca_ES-valencia
run1dump ckb_IQ.aff ckb_IQ.dic ckb_IQ
run1dump cs_CZ.aff cs_CZ.dic cs_CZ
run1dump da_DK.aff da_DK.dic da_DK
run1dump de_AT.aff de_AT.dic de_AT
run1dump de_BE.aff de_BE.dic de_BE
run1dump de_CH.aff de_CH.dic de_CH
run1dump de_DE.aff de_DE.dic de_DE
run1dump de_LI.aff de_LI.dic de_LI
run1dump de_LU.aff de_LU.dic de_LU
run1dump dz.aff dz.dic dz
run1dump dz_BT.aff dz_BT.dic dz_BT
run1dump el_GR.aff el_GR.dic el_GR
run1dump en_AU.aff en_AU.dic en_AU
run1dump en_CA.aff en_CA.dic en_CA
run1dump en_GB.aff en_GB.dic en_GB
run1dump en_ZA.aff en_ZA.dic en_ZA
run1dump es_AR.aff es_AR.dic es_AR
run1dump es_BO.aff es_BO.dic es_BO
run1dump es_CL.aff es_CL.dic es_CL
run1dump es_CO.aff es_CO.dic es_CO
run1dump es_CR.aff es_CR.dic es_CR
run1dump es_CU.aff es_CU.dic es_CU
run1dump es_DO.aff es_DO.dic es_DO
run1dump es_EC.aff es_EC.dic es_EC
run1dump es_ES.aff es_ES.dic es_ES
run1dump es_GT.aff es_GT.dic es_GT
run1dump es_HN.aff es_HN.dic es_HN
run1dump es_MX.aff es_MX.dic es_MX
run1dump es_NI.aff es_NI.dic es_NI
run1dump es_PA.aff es_PA.dic es_PA
run1dump es_PE.aff es_PE.dic es_PE
run1dump es_PR.aff es_PR.dic es_PR
run1dump es_PY.aff es_PY.dic es_PY
run1dump es_SV.aff es_SV.dic es_SV
run1dump es_UY.aff es_UY.dic es_UY
run1dump es_VE.aff es_VE.dic es_VE
run1dump et_EE.aff et_EE.dic et_EE
run1dump eu.aff eu.dic eu
run1dump eu_ES.aff eu_ES.dic eu_ES
run1dump eu_FR.aff eu_FR.dic eu_FR
run1dump fr.aff fr.dic fr
run1dump fr_BE.aff fr_BE.dic fr_BE
run1dump fr_CA.aff fr_CA.dic fr_CA
run1dump fr_CH.aff fr_CH.dic fr_CH
run1dump fr_FR.aff fr_FR.dic fr_FR
run1dump fr_LU.aff fr_LU.dic fr_LU
run1dump fr_MC.aff fr_MC.dic fr_MC
run1dump gd_GB.aff gd_GB.dic gd_GB
run1dump gl_ES.aff gl_ES.dic gl_ES
run1dump gu_IN.aff gu_IN.dic gu_IN
run1dump hi_IN.aff hi_IN.dic hi_IN
run1dump hr_HR.aff hr_HR.dic hr_HR
run1dump hu_HU.aff hu_HU.dic hu_HU
run1dump id_ID.aff id_ID.dic id_ID
run1dump is_IS.aff is_IS.dic is_IS
run1dump it_CH.aff it_CH.dic it_CH
run1dump it_IT.aff it_IT.dic it_IT
run1dump kk_KZ.aff kk_KZ.dic kk_KZ
run1dump kmr_Latn.aff kmr_Latn.dic kmr_Latn
run1dump ko.aff ko.dic ko
run1dump ko_KR.aff ko_KR.dic ko_KR
run1dump ku_SY.aff ku_SY.dic ku_SY
run1dump ku_TR.aff ku_TR.dic ku_TR
run1dump lo_LA.aff lo_LA.dic lo_LA
run1dump lt_LT.aff lt_LT.dic lt_LT
run1dump lv_LV.aff lv_LV.dic lv_LV
run1dump ml_IN.aff ml_IN.dic ml_IN
run1dump mn_MN.aff mn_MN.dic mn_MN
run1dump nb_NO.aff nb_NO.dic nb_NO
run1dump ne_NP.aff ne_NP.dic ne_NP
run1dump nl.aff nl.dic nl
run1dump nl_AW.aff nl_AW.dic nl_AW
run1dump nl_BE.aff nl_BE.dic nl_BE
run1dump nl_NL.aff nl_NL.dic nl_NL
run1dump nl_SR.aff nl_SR.dic nl_SR
run1dump nn_NO.aff nn_NO.dic nn_NO
run1dump oc_FR.aff oc_FR.dic oc_FR
run1dump pa_IN.aff pa_IN.dic pa_IN
run1dump pl_PL.aff pl_PL.dic pl_PL
run1dump pt_BR.aff pt_BR.dic pt_BR
run1dump pt_PT.aff pt_PT.dic pt_PT
run1dump ro_RO.aff ro_RO.dic ro_RO
run1dump si_LK.aff si_LK.dic si_LK
run1dump sk_SK.aff sk_SK.dic sk_SK
run1dump sl_SI.aff sl_SI.dic sl_SI
run1dump sr_Latn_RS.aff sr_Latn_RS.dic sr_Latn_RS
run1dump sr_ME.aff sr_ME.dic sr_ME
run1dump sr_RS.aff sr_RS.dic sr_RS
run1dump sv_FI.aff sv_FI.dic sv_FI
run1dump sv_SE.aff sv_SE.dic sv_SE
run1dump sw_KE.aff sw_KE.dic sw_KE
run1dump sw_TZ.aff sw_TZ.dic sw_TZ
run1dump te_IN.aff te_IN.dic te_IN
run1dump th_TH.aff th_TH.dic th_TH
run1dump tr_TR.aff tr_TR.dic tr_TR
run1dump uk_UA.aff uk_UA.dic uk_UA
run1dump uz_UZ.aff uz_UZ.dic uz_UZ
run1dump vi_VN.aff vi_VN.dic vi_VN
run1dump zu_ZA.aff zu_ZA.dic zu_ZA

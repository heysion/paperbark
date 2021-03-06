import os
# $1: path ov vdev (image)
# $2: pool name

def pool_create(path,pool_name):
    if path and pool_name:
        raise ZFSError('path or pool name is not null')
    cmd = "sudo zpool create -m legacy -o ashift=12 -O compression=on %s %s"%(pool_name,path)
    ret = os.system(cmd)
    cmd = "sudo zfs create %s/SNAPSHOTS"%(pool_name)
    ret = os.system(cmd)
    cmd = "sudo zfs create %s/STAGINGS"%(pool_name)
    ret = os.system(cmd)

# $1: pool name
def pool_destroy(pool_name):
    if pool_name :
        raise ZFSError('pool_destroy: pool name is not null')
    cmd = "sudo zpool destroy %s"%(pool_name)
    ret = os.system(cmd)

# # $1: pool name
def pool_is_active(pool_name):
    if pool_name :
        raise ZFSError("pool_is_active: pool name is not null")
    cmd = "sudo zpool list -H -o name %s &>/dev/null"%(pool_name)
    ret = os.system(cmd)

# # $1: image directory
# # $2: pool name
def pool_import(image_dir,pool_name):
    if image_dir and pool_name:
        raise ZFSError("pool_import: image directory or pool name is not null")
    cmd = "sudo zpool import -d %s -f %s &>/dev/null"%(image_dir,pool_name)
    ret = os.system(cmd)

# # $1: directory to search for pool
# pool_activate() {
#     local _pool_file=($1/*.zfs)
#     if [[ ! -f "$_pool_file" ]]; then
#         return 1
#     fi

#     _zfs_pool_name="${_pool_file##*/}"
#     _zfs_pool_name="${_zfs_pool_name%.zfs}"
#     _zfs_ds_snapshots="$_zfs_pool_name/SNAPSHOTS"
#     _zfs_ds_stagings="$_zfs_pool_name/STAGINGS"

#     if ! pool_is_active "$_zfs_pool_name"; then
#         pool_import "$1" "$_zfs_pool_name"
#     fi

#     zfs_cache_init
# }

# dataset_exists() {
#     zfs list -H -o name "$1" &>/dev/null
# }

# dataset_create() {
#     zfs create -o mountpoint=legacy -p "$1"
# }

# # $1: dataset name
# # $2: mount point
# dataset_mount() {
#     local _dataset="$1"; shift
#     local _mount_point="$1"; shift
#     mount -t zfs "$_dataset" "$_mount_point" "$@"
# }

# dataset_destroy() {
#     sudo zfs destroy -f "$1"
# }

# dataset_destroy_recursive() {
#     sudo zfs destroy -fR "$1"
# }

# # $1: dataset name
# # $2: variable name of dependents
# dataset_get_dependents() {
#     local _line
#     local -a _lines

#     while read _line; do
#         _lines+=("$_line")
#     done < <(zfs destroy -n "$_zfs_ds_snapshots/$1" 2>&1)

#     if [[ 0 == ${#_lines} ]]; then
#         return 1
#     fi

#     eval $2=\("\${_lines[@]:2:${#_lines[@]}-3}"\)
# }

# dataset_list() {
#     zfs list -r -H -o name -S creation -S name "$1"
# }

# # $1: dataset
# # $2: property name
# # $3: variable name of property value
# dataset_prop_get() {
#     local _fields=($(sudo zfs get "$2" -H "$1"))
#     eval $3=${_fields[2]}
# }

# # $1: dataset
# # $2: property name
# # $3: expected property value
# dataset_prop_value_is() {
#     local _fields=($(sudo zfs get "$2" -H "$1"))
#     [[ "$3" == "${_fields[2]}" ]]
# }

# # $1: dataset
# # $2: property name
# # $3: property value
# dataset_prop_set() {
#     sudo zfs set "$2"="$3" "$1"
# }

# # $1: dataset
# # $2: property name
# dataset_unset() {
#     sudo fs inherit "$2" "$1"
# }

# # $1: dataset
# # $2: callback, return false to stop enumerating.
# # $*: arguments for callback
# # return: true if callback never failed.
# dataset_enum() {
#     local _dataset="$1"; shift
#     local _callback="$1"; shift
#     while read line; do
#         if ! $_callback "$line" "$@"; then
#             return 1
#         fi
#     done < <(zfs list -r -H -o name -S creation -S name "$_dataset")
# }

# # $1: dataset
# dataset_in_stagings() {
#     str_has_prefix "$1" "$_zfs_ds_stagings"
# }

# # $1: dataset
# dataset_in_snapshots() {
#     str_has_prefix "$1" "$_zfs_ds_snapshots"
# }

# # $1: source dataset
# # $2: destination dataset
# dataset_move() {
#     zfs rename -p "$1" "$2"
# }

# ################
# #
# # snapshot id: ubuntu
# #              the snapshot id is non-unique id
# # versioned snapshot id: ubuntu:12.04
# #                        versioned snapshot id must be unique
# # normailized snapshot id: 3d0007ae-d9af-4898-ac9f-e0833a1571ff@ubuntu:1
# #                          normaized snapshot id is the one paperbark used to
# #                          map versioned snapshot id to zfs dataset, unique
# #
# ################

# # $1: snapshot id
# # $2: name of variable of snapshot name
# # $3: name of variable of snapshot version
# # $4: if snapshot id has only tag name part, use this value as tag version
# # return: true if version part of snapshot id is not empty, false if not
# snapshot_id_split() {
#     eval $2="${1%:*}"
#     eval $3="${1#${!2}}"
#     eval $3="${!3#:}"
#     if [[ -z "${!3}" ]]; then
#         eval $3="$4"
#     fi

#     [[ "${!3}" ]]
# }

# # $1: snapshot id
# snapshot_id_has_version() {
#     [[ "$1" == *:* ]]
# }

# # $1: normalized snapshot id
# snapshot_destroy() {
#     dataset_destroy "$_zfs_ds_snapshots/$1"
#     dataset_destroy "$_zfs_ds_snapshots/${1%@*}"
# }

# snapshot_destroy_recursive() {
#     dataset_destroy_recursive "$_zfs_ds_snapshots/${1%@*}"
# }

# # $1: normalized snapshot id
# snapshot_destroy_recursive_and_reclaim() {
#     snapshot_mark_destroyed "$1"
#     if snapshot_has_rdeps "$1"; then
#         return
#     fi

#     local _sdrr_target_snap="$1" _sdrr_tmp_snap
#     while snapshot_get_dep "$_sdrr_target_snap" _sdrr_tmp_snap; do
#         if snapshot_has_strong_rdeps "$_sdrr_tmp_snap"; then
#             break
#         fi

#         _sdrr_target_snap="$_sdrr_tmp_snap"
#     done

#     snapshot_destroy_recursive "$_sdrr_target_snap"
# }

# # $1: normalized snapshot id
# snapshot_is_marked_destroyed() {
#     [[ "${_zfs_snap_destroyed[$1]}" ]]
# }

# # $1: normalized snapshot id
# snapshot_mark_destroyed() {
#     snapshot_prop_set "$1" "pb:destroyed" "yes"
#     _zfs_snap_destroyed["$1"]="yes"
# }

# # $1: snapshot id
# # $2: snapshot version
# # $3: variable name of final snapshot id
# snapshot_id_add_version() {
#     if ! snapshot_id_has_version "$1"; then
#         eval $3="$1:$2"
#     else
#         eval $3="$1"
#     fi
# }

# # $1: snapshot id
# # $2: variable name of normailzed snapshot id, optional
# # return: true if snapshot exists, false if not
# snapshot_id_normalize() {
#     local _sin_snap_id="$1"
#     snapshot_id_add_version "$_sin_snap_id" latest _sin_snap_id
#     if [[ -z "${_zfs_snap_id_fs_map["${_sin_snap_id#*@}"]}" ]]; then
#         return 1
#     fi

#     if [[ "${_sin_snap_id#*@}" == "${_sin_snap_id}" ]]; then
#         _sin_snap_id="${_zfs_snap_id_fs_map[$_sin_snap_id]}@$_sin_snap_id"
#     fi

#     if [[ "$2" ]]; then
#         eval $2="$_sin_snap_id"
#     fi
# }

# # $1: callback, return false to stop enumerating.
# #    $1: normalized snapshot id
# # $*: arguments for callback
# snapshot_enum() {
#     local _callback="$1"; shift
#     local _snapshot
#     for _snapshot in ${_zfs_snaps[@]}; do
#         if ! $_callback "${_snapshot}" "$@"; then
#             return 1
#         fi
#     done
# }

# # $1: normalized source snapshot id
# # $2: destination snapshot id
# snapshot_rename() {
#     zfs rename "$_zfs_ds_snapshots/$1" "$_zfs_ds_snapshots/${1%@*}@$2"
# }

# # $1: fs
# # $2: snapshot id
# snapshot_create() {
#     local _fs="$1"; shift
#     local _snap_id="$1"; shift
#     zfs snapshot "$_zfs_ds_snapshots/$_fs@$_snap_id" "$@"
# }

# # $1: normalized snapshot id
# snapshot_exists() {
#     [[ "${1%@*}" == "${_zfs_snap_id_fs_map[${1#*@}]}" ]]
# }

# # $1: fs
# # $2: variable name of dataset
# snapshot_fs_exists() {
#     if [[ -z "${_zfs_snap_fs_id_map[$1]}" ]]; then
#         return 1
#     fi

#     if [[ "$2" ]]; then
#         eval $2="${_zfs_snap_fs_id_map[$1]}:$1"
#     fi
# }

# # $1: snapshot id
# # $2: variable name of dataset
# snapshot_to_dataset() {
#     _snapshot_to_dataset() {
#         if [[ "$1" == "$3" ]]; then
#             eval $4="$_zfs_ds_snapshots/$2@$1"
#             return 1
#         fi
#     }

#     if snapshot_enum _snapshot_to_dataset "$@"; then
#         return 1
#     fi
# }

# # $1: normalized snapshot id
# # $2: property name
# # $3: variable name of property value
# snapshot_prop_get() {
#     dataset_get "$_zfs_ds_snapshots/$1" "$2" "$3"
# }

# # $1: normalized snapshot id
# # $2: property name
# # $3: expected property value
# snapshot_prop_value_is() {
#     dataset_prop_value_is "$_zfs_ds_snapshots/$1" "$2" "$3"
# }

# # $1: normalized snapshot id
# # $2: property name
# # $3: property value
# snapshot_prop_set() {
#     dataset_prop_set "$_zfs_ds_snapshots/$1" "$2" "$3"
# }

# # $1: variable of newly created staging filesystem
# staging_create() {
#     local _fs=$(uuidgen)
#     dataset_create "$_zfs_ds_stagings/$_fs"
#     eval $1="$_fs"
# }

# # $1: staging id
# staging_destroy() {
#     dataset_destroy "$_zfs_ds_stagings/$1"
#     local _sd_key
#     for _sd_key in "${!_zfs_stags[@]}"; do
#         if [[ "${_zfs_stags[$_sd_key]}" == "$1" ]]; then
#             unset _zfs_stags[$_sd_key]
#             break
#         fi
#     done
#     for _sd_key in "${!_zfs_snap_rdeps[@]}"; do
#         _zfs_snap_rdeps[$_sd_key]="${_zfs_snap_rdeps[$_sd_key]//$1/}"
#     done
#     unset _zfs_stag_deps["$1"]
# }

# # $1: staging id
# staging_destroy_recursive_and_reclaim() {
#     local _sdrr_dep
#     if staging_has_dep "$1"; then
#         staging_get_dep "$1" _sdrr_dep
#     fi

#     staging_destroy "$1"

#     if [[ "$_sdrr_dep" ]] && snapshot_is_marked_destroyed "$_sdrr_dep"; then
#         snapshot_destroy_recursive_and_reclaim "$_sdrr_dep"
#     fi
# }

# # $1: staging id
# staging_has_dep() {
#     [[ "${_zfs_stag_deps[$1]}" ]]
# }

# # $1: staing id
# # $2: variable name of dependency
# staging_get_dep() {
#     eval $2="${_zfs_stag_deps[$1]}"
# }

# # $1: staging id
# # $2: variable name of dataset
# staging_exists() {
#     local _staging
#     for _staging in "${_zfs_stags[@]}"; do
#         if [[ "$1" != "$_staging" ]]; then
#             continue
#         fi

#         if [[ "$2" ]]; then
#             eval $2="$_zfs_ds_stagings/$1"
#         fi

#         return
#     done

#     return 1
# }

# # $1: callback, return false to stop enumerating.
# #     $1: staging fs
# # $*: arguments for callback
# # return: true if callback never failed.
# staging_enum() {
#     local _callback="$1"; shift
#     for fs in "${_zfs_stags[@]}"; do
#         $_callback "$fs" "$@"
#     done
# }

# # $1: filesystem
# # $2: prefix
# # $3: variable name of result dataset
# staging_move_to_snapshots() {
#     local _dest="$_zfs_ds_snapshots/$1"
#     zfs rename -p "$dataset_staggins/$1" "$_dest"

#     if [[ "$3" ]]; then
#         eval $3="$_dest"
#     fi
# }

# # $1: snapshot filesystem
# # $2: optional. variable name of resulting dataset
# snapshot_fs_to_stagings() {
#     local _dest_dataset="$_zfs_ds_stagings/$1"
#     dataset_move "$_zfs_ds_snapshots/$1" "$_dest_dataset"
#     if [[ "$2" ]]; then
#         eval $2="$_dest_dataset"
#     fi
# }

# # $1: the snapshot to be sent, or, the parent snapshot
# # $2: optional, the child snapshot to be sent incrementally
# snapshot_send() {
#     local _ss_cmd
#     if [[ 1 == $# ]]; then
#         _ss_cmd="sudo zfs send $_zfs_ds_snapshots/$1"
#     else
#         _ss_cmd="sudo zfs send -I $_zfs_ds_snapshots/$1 $_zfs_ds_snapshots/$2"
#     fi

#     $_ss_cmd
# }

# #
# # if variable report_progress=yes, shows receiving progress
# #
# # $1: progress callback
# #     $1: normalized snapshot id
# #     $2: progress
# # $@: normalized snapshot id to be sent
# snapshot_send_all() {
#     local _ssa_callback="$1"; shift
#     if [[ 0 == $# ]]; then
#         return
#     fi

#     local -a _ssa_progress_args=(--wait --buffer-size 32M)
#     if [[ -z "$report_progress" ]]; then
#         _ssa_progress_args+=(--quiet)
#     fi

#     local _ssa_parent
#     snapshot_get_dep "$1" _ssa_parent || true

#     local _ssa_count=1
#     while (( 0 < $# )); do
#         $_ssa_callback "$1" "$_ssa_count" >&2

#         snapshot_send $_ssa_parent $1
#         _ssa_parent="$1"

#         (( _ssa_count++ ))

#         shift
#     done | lbzip2 -z -c | pv "${_ssa_progress_args[@]}"
# }

# snapshot_receive() {
#     sudo zfs recv -d $_zfs_pool_name
# }

# #
# # if variable report_progress=yes, shows receiving progress
# #
# # $1: progress callback
# #     $1: normalized snapshot id
# #     $2: progress
# # $@: expected normalized snpahost id to be received
# snapshot_receive_all() {
#     local _sra_callback="$1"; shift
#     local _sra_count=1

#     local -a _sra_progress_args=(--wait --buffer-size 32M)
#     if [[ -z "$report_progress" ]]; then
#         _sra_progress_args+=(--quiet)
#     fi

#     lbzip2 -d -c | pv "${_sra_progress_args[@]}" | while [[ 0 != $# ]]; do
#         $_sra_callback "$1" "$_sra_count" >&2

#         snapshot_receive "$1"

#         (( _sra_count++ ))

#         shift
#     done
# }

# # $1: normalized snapshot id
# snapshot_has_dep() {
#     [[ "${_zfs_snap_deps[$1]}" ]]
# }

# # $1: normalized snapshot id
# # $2: variable name of parent snapshot
# snapshot_get_dep() {
#     if ! snapshot_has_dep "$1"; then
#         return 1
#     fi

#     eval $2="${_zfs_snap_deps[$1]}"
# }

# # $1: normailzed snapshot id
# # $2: variable name of resulting array of snapshots, start from oldest parent
# snapshot_series_get() {
#     local _ssg_snapshot="$1"
#     local -a _ssg_snapshots=("$_ssg_snapshot")
#     while snapshot_get_dep "$_ssg_snapshot" _ssg_snapshot; do
#         _ssg_snapshots=("$_ssg_snapshot" "${_ssg_snapshots[@]}")
#     done

#     eval $2=\("${_ssg_snapshots[@]}"\)
# }

# # $1: variable name of tailored result
# # $@: snapshot series
# snapshot_series_send_and_receive_diff() {
#     local _result="$1"; shift

#     echo "$@"

#     snapshot_series_receive_diff "$_result"
# }

# # $1: variable name of tailored snapshot series
# snapshot_series_receive_diff() {
#     local _line
#     read _line

#     eval $1=\($_line\)
# }

# # $1: variable name of tailored result
# # $@: snapshot series
# snapshot_series_gen_diff() {
#     local _result="$1"; shift

#     while [[ 0 != $# ]]; do
#         if ! snapshot_exists "$1"; then
#             break
#         fi
#         shift
#     done

#     echo "$@"

#     eval $_result=\("$@"\)
# }

# # $1: normalized snapshot id or staging filesystem id
# # $2: directory to mount file system to
# snapshot_or_staging_mount() {
#     local _ds
#     if [[ "$1" != "${1%@*}" ]]; then
#         _ds="$_zfs_ds_snapshots/${1#@*}"
#     else
#         _ds="$_zfs_ds_stagings/$1"
#     fi

#     dataset_mount "$_ds" "$2"
# }

# # $1: normalized snapshot id or staging filesystem id
# snapshot_or_staging_to_tar() {
#     local _mount_point=$(mktemp -d)
#     cleanup_stack_push "rmdir $_mount_point"

#     snapshot_or_staging_mount "$1" "$_mount_point"
#     cleanup_stack_push "umount $_mount_point"

#     tar -cp -C "$_mount_point" . | pv -W

#     cleanup_stack_pop
#     cleanup_stack_pop
# }

# # $1: normalized snapshot id
# snapshot_is_deleted() {
#     [[ "${_zfs_snap_destroyed[$1]}" ]]
# }

# # $1: normalized snapshot id
# snapshot_has_rdeps() {
#     [[ "${_zfs_snap_rdeps[$1]}" ]]
# }

# # $1: normalized snapshot id
# # $2: variable name of reverse dependencies
# snapshot_get_rdeps() {
#     eval $2=\("${_zfs_snap_rdeps[$1]}"\)
# }

# # $1: normalized snapshot id
# # $2: normalized snapshot id to check to see if it's $1's rdep
# snapshot_is_direct_rdep() {
#     [[ "$1" == "${_zfs_snap_deps[$2]}" ]]
# }

# # $1: callback
# #   return: 0 keep going. 1 termiate. 2 skip current branch
# # $2: normalized snapshot id
# snapshot_foreach_rdeps() {
#     _snapshots_foreach_rdeps() {
#         local _sfr_exit_code
#         for _sfr_rdep in "${@:1}"; do
#             set +o errexit
#             $_sfr_callback "$_sfr_rdep" "${_sfr_extra_args[@]}"
#             _sfr_exit_code=$?
#             set -o errexit

#             case $_sfr_exit_code in
#                 1)
#                     return 1
#                     ;;
#                 2)
#                     continue
#                     ;;
#             esac

#             if ! str_find "$_sfr_rdep" "@"; then
#                 continue
#             fi

#             snapshot_get_rdeps "$_sfr_rdep" _sfr_rdeps
#             if [[ 0 == ${#_sfr_rdeps[@]} ]]; then
#                 continue
#             fi

#             if ! _snapshots_foreach_rdeps "${_sfr_rdeps[@]}"; then
#                 return 1
#             fi
#         done
#     }

#     local _sfr_callback="$1"; shift
#     local _sfr_rdep="$1"; shift
#     local -a _sfr_extra_args=("$@")
#     _snapshots_foreach_rdeps "$_sfr_rdep"
# }

# # a strong rdep (reverse dependency) is a reverse depenedency which
# # doesn't marked as destroyed
# # $1: normalized snapshot id
# snapshot_has_strong_rdeps() {
#     _snapshot_has_strong_rdeps() {
#         if str_find "$1" '@'; then
#             snapshot_is_marked_destroyed "$_sfr_rdep"
#         else
#             ! staging_exists "$1"
#         fi
#     }

#     if snapshot_foreach_rdeps _snapshot_has_strong_rdeps "$@"; then
#         return 1
#     fi
# }

# # $1: callback
# # $2: normalized snapshot id
# # $3: depth. -1 means no depth limitation
# snapshot_foreach_deps() {
#     _notify_deps() {
#         if [[ "$1" == "$_sfd_origin" || "$1" == "$_sfd_parent" ]]; then
#             return 2
#         fi
#         $_sfd_callback "$1" "${_sfd_ext_extra_args[@]}"
#     }

#     _snapshot_foreach_deps() {
#         if [[ 0 == $2 ]]; then
#             return
#         fi

#         snapshot_foreach_rdeps _notify_deps "$1"
#         if ! $_sfd_callback "$1" "${_sfd_ext_extra_args[@]}"; then
#             return 1
#         fi

#         _sfd_parent="$1"
#         if snapshot_get_dep "$1" _sfd_curr; then
#             _snapshot_foreach_deps "$_sfd_curr" $(($2 - 1))
#         fi
#     }

#     local _sfd_callback="$1"
#     local -r _sfd_origin="$2"
#     local _sfd_parent="$2"
#     local -i _sfd_depth="$3"
#     local _sfd_ext_extra_args=("${@:4}")

#     local _sfd_curr
#     if snapshot_get_dep "$2" _sfd_curr; then
#         _snapshot_foreach_deps "$_sfd_curr" "$_sfd_depth"
#     fi
# }

# # a strong dep (dependency) is a depenedency which
# # doesn't marked as destroyed
# # $1: normalized snapshot id
# # $2: depth. -1 means no depth limitation
# snapshot_has_strong_deps() {
#     _snapshot_has_strong_deps() {
#         snapshot_is_marked_destroyed "$1"
#     }

#     ! snapshot_foreach_deps _snapshot_has_strong_deps "$@"
# }

# # $1: normalized snapshot id
# # $2: variable name of staging filesystem
# staging_clone_from_snapshot() {
#     eval $2=$(uuidgen)
#     zfs clone "$_zfs_ds_snapshots/$1" "$_zfs_ds_stagings/${!2}"
# }

# # $1: staging fs
# # $2: variale name of mount point
# staging_mount() {
#     local _mount_point=$(mktemp -d /tmp/$pb_exec-$$-XXXXXX)
#     cleanup_stack_push "rmdir '$_mount_point'"

#     mount -t zfs "$_zfs_ds_stagings/$1" "$_mount_point"
#     eval $2="${_mount_point}"
# }

# # $1: staging filesystem
# # $2: variable name of resulting dataset
# staging_move_to_snapshots() {
#     local _dest_dataset="$_zfs_ds_snapshots/$1"
#     dataset_move "$_zfs_ds_stagings/$1" "$_dest_dataset"
#     if [[ "$2" ]]; then
#         eval $2="$_dest_dataset"
#     fi
# }

# # $1: partial staging fs id to be normalized
# # $2: variable name of normalized staging fs id
# staging_id_normalize() {
#     if (( 6 > ${#1} )); then
#         return 1
#     fi

#     local _sin_norm_id
#     for _sin_norm_id in "${_zfs_stags[@]}"; do
#         if [[ $_sin_norm_id == $1* ]]; then
#             eval $2="$_sin_norm_id"
#             return
#         fi
#     done

#     return 1
# }

# # $1: partial staging fs id to be normalized, at least 6 characters
# # $2: variable name of normalized staging fs id
# staging_id_check_and_normalize()
# {
#     if (( 6 > ${#1} )); then
#         return 1
#     fi

#     staging_id_normalize "$@"
# }

# zfs_cache_init() {
#     if [[ "$_zfs_cache_inited" ]]; then
#         return
#     fi

#     local _line
#     while read _line; do
#         _line="${_line#$_zfs_ds_snapshots}"
#         _line="${_line#/}"
#         if [[ -z "$_line" ]]; then
#             continue
#         fi

#         _zfs_snaps+=("$_line")
#         _zfs_snap_id_fs_map["${_line#*@}"]="${_line%@*}"
#         if [[ "${_zfs_snap_fs_id_map["${_line%@*}"]}" ]]; then
#             _zfs_snap_fs_id_map["${_line%@*}"]+=" "
#         fi
#         _zfs_snap_fs_id_map["${_line%@*}"]+="${_line#*@}"
#     done < <(sudo zfs list -H -r -t snapshot -o name -S creation $_zfs_ds_snapshots)

#     while read _line; do
#         local _fields=($_line)
#         _fields[0]="${_fields[0]#$_zfs_ds_snapshots}"
#         _fields[0]="${_fields[0]#/}"
#         if [[ -z "${_fields[0]}" ]]; then
#             continue
#         fi

#         if [[ '-' != "${_fields[1]}" ]]; then
#             local _snap_id="${_fields[0]}@${_zfs_snap_fs_id_map[${_fields[0]}]}"
#             _zfs_snap_deps["$_snap_id"]="${_fields[1]#$_zfs_ds_snapshots/}"
#         fi
#     done < <(sudo zfs list -H -r -o name,origin -S creation $_zfs_ds_snapshots)

#     while read _line; do
#         local _fields=($_line)
#         if [[ 1 == "${#_fields[@]}" ]]; then
#             continue
#         fi

#         _fields[0]="${_fields[0]#$_zfs_ds_snapshots}"
#         _fields[0]="${_fields[0]#/}"
#         if [[ -z "${_fields[0]}" ]]; then
#             continue
#         fi

#         if [[ '-' != "${_fields[1]}" ]]; then
#             _zfs_snap_destroyed["${_fields[0]}"]=yes
#         fi

#         local _dataset
#         local -a _rdeps
#         for _dataset in ${_fields[2]//,/ }; do
#             local _fs="${_dataset#*/*/}"
#             if dataset_in_stagings "$_dataset"; then
#                 _rdeps+=("$_fs")
#             else
#                 local _snap_id
#                 for _snap_id in ${_zfs_snap_fs_id_map[$_fs]}; do
#                     _rdeps+=("$_fs@$_snap_id")
#                 done
#             fi
#         done

#         _zfs_snap_rdeps["${_fields[0]}"]="${_rdeps[*]}"
#         unset _rdeps
#     done < <(sudo zfs list -H -r -o name,pb:destroyed,clones -t snap $_zfs_ds_snapshots)

#     while read _line; do
#         _fields=($_line)
#         _fields[0]="${_fields[0]#$_zfs_ds_stagings}"
#         _fields[0]="${_fields[0]#/}"
#         if [[ -z "${_fields[0]}" ]]; then
#             continue
#         fi

#         _zfs_stags+=("${_fields[0]}")
#         if [[ '-' != "${_fields[1]}" ]]; then
#             _zfs_stag_deps["${_fields[0]}"]="${_fields[1]#$_zfs_ds_snapshots/}"
#         fi
#     done < <(sudo zfs list -H -r -o name,origin -S creation $_zfs_ds_stagings)

#     _zfs_cache_inited=yes
# }

# zfs_cache_reinit() {
#     unset _zfs_cache_inited
#     zfs_cache_init
# }

# dep_add zfs zpool mount

# declare -g _zfs_cache_inited
# declare -ga _zfs_snaps
# declare -gA _zfs_snap_deps
# declare -gA _zfs_snap_rdeps
# declare -gA _zfs_snap_destroyed
# declare -gA _zfs_snap_id_fs_map
# declare -gA _zfs_snap_fs_id_map
# declare -ga _zfs_stags
# declare -gA _zfs_stag_deps
# declare -g _zfs_ds_snapshots
# declare -g _zfs_ds_stagings
# declare -g _zfs_pool_name

###
### start_browserify.pp, compile jsx into javascript.
###
class compiler::start_browserify {
    include compiler::webcompilers

    ## variables
    $hiera_general   = lookup('general')
    $root_dir        = $hiera_general['root']
    $environment     = $hiera_general['environment']
    $dev_env_path    = "${root_dir}/puppet/environment/${environment}"

    ## manually compile
    exec { 'browserify':
        command  => "./browserify ${root_dir}",
        cwd      => "${dev_env_path}/modules/compiler/scripts",
        path     => '/usr/bin',
        provider => shell,
        require  => Class['compiler::webcompilers'],
    }
}
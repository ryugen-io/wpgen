function wpgen --description 'Wallpaper generator'
    # Check if wpgen is installed (pipx)
    if not command -v wpgen &>/dev/null
        echo "Error: wpgen not installed"
        echo "Run: cd ~/code/github.com/ryugen-io/wpgen && ./install.sh"
        return 1
    end

    # Just pass through to the actual command
    command wpgen $argv
end

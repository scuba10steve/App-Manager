if [[ "$(conda env list)" == *"default"* ]]; then
    conda env remove -n default
fi

if [[ -f environment.yml ]]; then
    conda env create -f=environment.yml
fi

# OSMINT

OpenStreetMap INTelligence.

## Usage

First store data into the local cache in order to avoid re-fetching it for every plot.

Use the `--help` flag on any command to get detailed information and options on its usage.

### Download data

#### Changesets

Add changesets to the cache with the following command:

```bash
python3 main.py download changesets ${USERNAME}
```

### Plot

#### Heatmap

To plot a heatmap of changesets first load the changesets into the cache (see "Download data" -> "Changesets")

The following command will plot an interactive world map with the changesets and open it in your default browser:

```bash
python3 main.py plot heatmap ${USERNAME}
```
from pollination_dsl.dag import Inputs, DAG, task, Outputs
from dataclasses import dataclass
from typing import Dict, List
from pollination.honeybee_energy.settings import SimParDefault
from pollination.honeybee_energy.simulate import SimulateModel
from pollination.honeybee_energy.result import EnergyUseIntensity


# input/output alias
from pollination.alias.inputs.model import hbjson_model_input
from pollination.alias.inputs.simulation import energy_simulation_parameter_input


@dataclass
class CustomEnergySimEntryPoint(DAG):
    """Custom energy sim entry point."""

    # inputs
    model = Inputs.file(
        description='A Honeybee model in HBJSON file format.',
        extensions=['json', 'hbjson'],
        alias=hbjson_model_input
    )

    epw = Inputs.file(
        description='EPW weather file to be used for the energy simulation.',
        extensions=['epw']
    )

    sim_par = Inputs.file(
        description='SimulationParameter JSON that describes the settings for the '
        'simulation. Note that this SimulationParameter should usually contain '
        'design days. If it does not, the annual EPW data be used to generate '
        'default design days, which may not be as representative of the climate as '
        'those from a DDY file.', extensions=['json'],
        alias=energy_simulation_parameter_input
    )

    # tasks
    @task(template=SimulateModel)
    def run_simulation(self, model=model, epw=epw, sim_par=sim_par) -> List[Dict]:
        return [
            {'from': SimulateModel()._outputs.idf, 'to': 'model.idf'},
            {'from': SimulateModel()._outputs.sql, 'to': 'eplusout.sql'},
            {'from': SimulateModel()._outputs.zsz, 'to': 'epluszsz.csv'},
            {'from': SimulateModel()._outputs.html, 'to': 'eplustbl.htm'},
            {'from': SimulateModel()._outputs.err, 'to': 'eplusout.err'}
        ]

    # outputs
    idf = Outputs.file(
        source='model.idf', description='The IDF model used in the simulation.'
    )

    sql = Outputs.file(
        source='eplusout.sql',
        description='The result SQL file output by the simulation.'
    )

    zsz = Outputs.file(
        source='epluszsz.csv', description='The result CSV with the zone loads '
        'over the design day output by the simulation.'
    )

    html = Outputs.file(
        source='eplustbl.htm',
        description='The result HTML page with summary reports output by the simulation.'
    )

    err = Outputs.file(
        source='eplusout.err',
        description='The error report output by the simulation.'
    )

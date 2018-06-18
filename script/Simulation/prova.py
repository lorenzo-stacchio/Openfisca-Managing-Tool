import sys
from openfisca_italy import italy_taxbenefitsystem
from openfisca_italy import entita


def init_profile(scenario):
    scenario.init_single_entity(
        period = '2017',
        parent1 = dict(
            RN4_reddito_imponibile = 10000,
        )
    )
    return scenario


# main
tax_benefit_system = italy_taxbenefitsystem.ItalyTaxBenefitSystem() #prendi il sistema di tasse e benefici
variables = tax_benefit_system.get_variables(entity = entita.Persona)
print len(variables)
# scenario normale
print "\nCreazione ed inizializzazine dello scenario di tasse e benefici normale"
simple_scenario = tax_benefit_system.new_scenario() # nuovo scenario normale
simple_scenario = init_profile(simple_scenario) # inizializzo lo scenario con la situazione per calcolare la detrazione per la persona
print "Simulazione dello scenario di tasse e benefici normale"
simulation = simple_scenario.new_simulation() # nuova simulazione per lo scenario normale
# Print values
print('Irpef Lorda con sistema senza riforma:')
print(simulation.calculate('RN5_irpef_lorda','2017'))

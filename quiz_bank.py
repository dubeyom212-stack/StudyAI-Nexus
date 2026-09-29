"""Original starter questions. No runtime model call; answer keys stay server-side."""
import random


def q(topic, prompt, correct, wrong, explanation):
    return dict(topic=topic, prompt=prompt, options=[correct, *wrong], correct=0, explanation=explanation)


def question_bank(subject):
    if subject in {'AP Calculus AB', 'AP Calculus BC'}:
        rows = []
        for n in range(2, 12):
            rows.append(q('Derivatives', f'For f(x) = x^{n}, what is f\'(1)?', str(n), ['0', '1', str(n + 1)],
                          f'The power rule gives f\'(x) = {n}x^{n-1}. At x = 1, this equals {n}. The exponent becomes a coefficient before decreasing by one.'))
            rows.append(q('Definite integrals', f'Evaluate the integral of {n}x from x = 0 to x = 2.', str(2*n), [str(n), str(4*n), '0'],
                          f'An antiderivative is {n}x²/2. Evaluating at the upper bound gives {2*n}; subtracting the value at zero changes nothing.'))
            rows.append(q('Limits', f'What is the limit of (x² − {n*n})/(x − {n}) as x approaches {n}?', str(2*n), ['0', str(n), 'The limit does not exist'],
                          f'Factor the numerator as (x − {n})(x + {n}). For x ≠ {n}, the quotient equals x + {n}, which approaches {2*n}. The original function is undefined at the point, but its limit exists.'))
        return rows
    return [q(*row) for row in BANK.get(subject, [])]


BANK = {
'AP Biology': [
('Enzymes', 'The same enzyme is tested at 20°C, 35°C, and 70°C. Initial rates are 4, 9, and 1 units/min. Which explanation best accounts for the low rate at 70°C?', 'Heat altered the enzyme’s active-site shape', ['The enzyme was consumed as a reactant', 'Higher temperature always lowers molecular motion', 'The reaction must have reached equilibrium before it began'], 'High heat can disrupt interactions maintaining protein shape. An altered active site may bind substrate less effectively. Enzymes are catalysts and are not consumed in each reaction.'),
('Membranes', 'A cell permeable to water but not sucrose contains 0.1 M sucrose. It is placed in 0.5 M sucrose. What is the initial net movement of water?', 'Out of the cell', ['Into the cell', 'No net movement', 'Water becomes sucrose'], 'Water moves toward the side with higher solute concentration across this selectively permeable membrane. The outside solution is hypertonic relative to the cell.'),
('Genetics', 'Two heterozygotes, Aa and Aa, are crossed. With complete dominance, what fraction of offspring are expected to show the recessive phenotype?', '1/4', ['1/2', '3/4', 'All offspring'], 'The genotype combinations are AA, Aa, Aa, and aa. Only aa expresses the recessive phenotype under complete dominance.'),
('Experimental design', 'Plants receive either fertilizer A or no fertilizer. Which condition should be held constant to isolate the fertilizer effect?', 'Light exposure', ['The fertilizer treatment itself', 'The resulting plant height', 'The measured growth rate'], 'Light can affect growth independently of fertilizer, so it should be controlled. Height and growth rate are outcomes to measure, not force to be equal.'),
('Evolution', 'After antibiotic treatment, resistant bacteria become more common. Which explanation best fits natural selection?', 'Resistant variants survived and reproduced more successfully', ['Every bacterium chose to become resistant', 'The antibiotic produced exactly the mutations needed in every cell', 'Resistance appeared because bacteria stopped reproducing'], 'Selection changes variant frequencies through differences in survival and reproduction. It does not require organisms to choose traits or mutations to anticipate needs.'),
('Cell respiration', 'In aerobic respiration, what directly accepts electrons at the end of the electron transport chain?', 'Oxygen', ['Glucose', 'Carbon dioxide', 'ATP'], 'Oxygen is the final electron acceptor and combines with electrons and hydrogen ions to form water. Without it, electron flow through the chain stalls.'),
('Cell division', 'During which process do homologous chromosome pairs separate?', 'Meiosis I', ['Mitosis metaphase', 'DNA replication', 'Meiosis II'], 'Homologous chromosomes separate in anaphase I. Sister chromatids separate in anaphase II and in mitotic anaphase.'),
('Gene expression', 'A DNA template triplet is 3′-TAC-5′. Which mRNA triplet is transcribed?', '5′-AUG-3′', ['5′-TAC-3′', '5′-ATG-3′', '5′-UAC-3′'], 'RNA is complementary and antiparallel to the template. T pairs with A, A with U, and C with G; RNA uses uracil rather than thymine.'),
('Ecology', 'An ecosystem’s producers store 10,000 kJ. Assuming 10% transfer at each step, how much reaches secondary consumers?', '100 kJ', ['1,000 kJ', '10 kJ', '10,000 kJ'], 'Primary consumers receive 1,000 kJ, then secondary consumers receive 10% of that: 100 kJ. The question specifies two transfers.'),
('Cell signaling', 'A signal binds a receptor on a cell surface, but an internal relay protein is inactive. Which outcome is most likely?', 'The downstream response is reduced despite receptor binding', ['The signal must enter the nucleus directly', 'Every downstream protein activates normally', 'DNA replication becomes independent of enzymes'], 'Reception and transduction are separate steps. Binding a receptor does not guarantee a response if an essential relay in the pathway is blocked.')],
'AP Chemistry': [
('Stoichiometry', 'For 2H₂ + O₂ → 2H₂O, 3 mol H₂ reacts with 1 mol O₂. What is the maximum amount of water formed?', '2 mol', ['1 mol', '3 mol', '4 mol'], 'One mole of O₂ requires 2 mol H₂ and produces 2 mol H₂O. Oxygen is limiting; 1 mol H₂ remains.'),
('Solutions', 'What is the molarity of 0.50 mol solute in 2.0 L of solution?', '0.25 M', ['1.0 M', '2.5 M', '4.0 M'], 'Molarity is moles divided by liters of solution: 0.50/2.0 = 0.25 mol/L.'),
('Acids and bases', 'A solution has [H⁺] = 1 × 10⁻³ M. What is its pH?', '3', ['−3', '11', '0.001'], 'pH = −log₁₀[H⁺]. The logarithm is −3, so pH is 3.'),
('Equilibrium', 'At constant temperature, a catalyst is added to a reaction at equilibrium. What happens to the equilibrium constant K?', 'It stays the same', ['It increases', 'It decreases', 'It becomes zero'], 'A catalyst changes reaction rates by lowering activation barriers. It does not change the equilibrium constant or the equilibrium composition.'),
('Gas laws', 'An ideal gas in a sealed rigid container is heated from 300 K to 600 K. What happens to its pressure?', 'It doubles', ['It halves', 'It stays the same', 'It quadruples'], 'With amount and volume fixed, P is proportional to absolute temperature. The temperature doubles, so pressure doubles.'),
('Intermolecular forces', 'Which interaction explains why water has a higher boiling point than hydrogen sulfide?', 'Stronger hydrogen bonding between water molecules', ['Covalent bonds between all neighboring water molecules', 'Water has no intermolecular forces', 'Water molecules are heavier'], 'Water’s O–H groups form strong intermolecular hydrogen bonds. Boiling separates molecules; it does not break the covalent O–H bonds within each molecule.'),
('Thermochemistry', 'A reaction releases heat to its surroundings at constant pressure. What is the sign of its enthalpy change?', 'Negative', ['Positive', 'Always zero', 'Impossible to determine from heat release'], 'An exothermic process transfers heat out of the system, so its enthalpy decreases and ΔH is negative.'),
('Kinetics', 'Doubling [A] while holding other concentrations fixed makes the initial reaction rate four times larger. What is the order with respect to A?', 'Second order', ['Zero order', 'First order', 'Fourth order'], 'If rate is proportional to [A]^n, doubling [A] multiplies rate by 2^n. Since 2^n = 4, n = 2.'),
('Redox', 'In Zn → Zn²⁺ + 2e⁻, what happens to zinc?', 'It is oxidized', ['It is reduced', 'It gains two electrons', 'Its oxidation number decreases'], 'Oxidation is electron loss. Zinc’s oxidation number increases from 0 to +2.'),
('Buffers', 'Which mixture can act as a buffer?', 'A weak acid and its conjugate base', ['Only a strong acid in water', 'Only sodium chloride in water', 'Pure water with no added solute'], 'A weak acid can consume added base, and its conjugate base can consume added acid. Both components are needed in appreciable amounts.')],
'AP Environmental Science': [
('Energy', 'A device receives 500 J and delivers 100 J of useful energy. What is its efficiency?', '20%', ['5%', '80%', '100%'], 'Efficiency = useful output/input × 100 = 100/500 × 100 = 20%. The remaining input does not become useful output.'),
('Water quality', 'Fertilizer runoff enters a lake and an algal bloom follows. Why may dissolved oxygen later decline?', 'Decomposers consume oxygen while breaking down dead algae', ['Phosphorus directly turns oxygen into nitrogen', 'All algae stop respiring', 'Water can no longer dissolve any gases'], 'Excess nutrients stimulate growth. When biomass dies, microbial decomposition increases oxygen demand, potentially causing hypoxia.'),
('Population', 'A population has 40 births, 25 deaths, 10 immigrants, and 5 emigrants in one year. What is its net change?', 'Increase of 20', ['Increase of 30', 'Decrease of 20', 'Increase of 10'], 'Net change = births + immigration − deaths − emigration = 40 + 10 − 25 − 5 = 20.'),
('Climate', 'Which property allows carbon dioxide to contribute to warming?', 'It absorbs some outgoing infrared radiation', ['It absorbs all incoming visible light', 'It destroys gravity', 'It prevents all evaporation'], 'Earth emits infrared radiation. Greenhouse gases absorb and emit portions of that radiation, affecting the energy escaping to space.'),
('Energy resources', 'Which electricity source uses heat from Earth’s interior?', 'Geothermal', ['Photovoltaic solar', 'Wind', 'Tidal'], 'Geothermal systems use subsurface heat. Solar panels use sunlight, wind turbines use moving air, and tidal systems use water movement.'),
('Food webs', 'A persistent, fat-soluble pollutant becomes more concentrated at higher trophic levels. What is this called?', 'Biomagnification', ['Eutrophication', 'Nitrogen fixation', 'Primary succession'], 'Biomagnification is increasing concentration across trophic levels as predators consume contaminated prey. Bioaccumulation describes buildup within an organism over time.'),
('Agriculture', 'What is a likely benefit of planting cover crops between harvests?', 'Reduced soil erosion', ['Elimination of all water use', 'Permanent removal of all pests', 'Increased exposure of bare soil'], 'Roots help hold soil and foliage reduces the impact of rainfall. Cover crops can also reduce nutrient loss, but they do not eliminate water use or all pests.'),
('Biodiversity', 'A large habitat is divided by roads into isolated patches. What is a likely consequence?', 'Reduced movement and gene flow between populations', ['Guaranteed increase in genetic diversity in every patch', 'Elimination of all edge effects', 'Immediate speciation of every organism'], 'Fragmentation can isolate populations and restrict dispersal. Wildlife corridors can help restore movement between patches.'),
('Waste', 'Which action most directly reduces material use before waste is produced?', 'Reusing a durable bottle instead of buying disposable bottles', ['Incinerating more disposable bottles', 'Expanding a landfill', 'Transporting waste farther away'], 'Reuse reduces demand for new disposable products. Disposal methods handle waste after production and do not directly prevent material use.'),
('Experimental design', 'Two streams differ in temperature, flow, and fertilizer exposure. Why is attributing their oxygen difference only to fertilizer difficult?', 'Temperature and flow are potential confounding variables', ['Dissolved oxygen cannot be measured', 'Fertilizer can never affect streams', 'A sample size of two proves causation'], 'Several conditions vary together, so their effects cannot be separated from this comparison alone. Control or account for those variables when testing fertilizer effects.')],
'AP Statistics': [
('Sampling', 'A school surveys only students attending an optional tutoring session about schoolwide homework time. What is the main concern?', 'Selection bias', ['Guaranteed random sampling', 'A census of all students', 'Double-blind assignment'], 'Tutoring attendees may differ systematically from other students. A large response rate within this group does not make it representative of the entire school.'),
('Experimental design', 'Why randomly assign participants to treatment groups?', 'To help balance potential confounders across groups', ['To guarantee the sample represents every population', 'To eliminate all sampling variability', 'To force equal outcomes'], 'Random assignment supports causal comparisons by balancing confounding variables in expectation. Random sampling serves the different goal of population generalization.'),
('Probability', 'Independent events A and B have probabilities 0.4 and 0.5. What is P(A and B)?', '0.20', ['0.90', '0.10', '0.80'], 'For independent events, multiply the probabilities: 0.4 × 0.5 = 0.20. Adding would not calculate the intersection.'),
('Descriptive statistics', 'A data set has values 2, 3, 4, 5, and 100. Which measure of center is less affected by the high outlier?', 'Median', ['Mean', 'Range', 'Standard deviation'], 'The median is the middle value, 4. The mean uses every value’s magnitude and is pulled upward by 100. Range and standard deviation measure spread.'),
('Inference', 'A 95% confidence-interval procedure is used repeatedly on random samples. What does 95% describe?', 'About 95% of intervals from repeated samples contain the fixed parameter', ['95% of observations lie inside every interval', 'Each sample mean equals the population mean with 95% probability', 'The parameter changes between samples'], 'Confidence level describes the long-run coverage of the procedure. It does not describe the fraction of individual data points in an interval.'),
('Hypothesis tests', 'A test gives p = 0.03 and the preselected significance level is 0.05. What decision follows?', 'Reject the null hypothesis', ['Prove the null hypothesis', 'Accept the alternative with certainty', 'Change the significance level to 0.01'], 'Since p < α, reject the null. This decision is evidence against the null under the test assumptions, not proof or certainty.'),
('Regression', 'A regression model predicts y = 2 + 3x. An observation at x = 4 has y = 16. What is its residual?', '2', ['−2', '14', '16'], 'The predicted value is 2 + 3(4) = 14. Residual = observed − predicted = 16 − 14 = 2.'),
('Sampling distributions', 'For independent observations with fixed population standard deviation, increasing sample size from 25 to 100 does what to the standard error of the mean?', 'Halves it', ['Doubles it', 'Leaves it unchanged', 'Divides it by four'], 'Standard error is σ/√n. Quadrupling n doubles its square root, so standard error is divided by two.'),
('Probability', 'A fair coin is flipped three times independently. What is the probability of three heads?', '1/8', ['1/2', '1/3', '3/8'], 'Multiply the three independent probabilities: (1/2)³ = 1/8. The probability of exactly two heads would be 3/8.'),
('Association', 'Ice cream sales and swimming incidents rise together in summer. Why does this not establish that ice cream causes incidents?', 'Warm weather may influence both variables', ['Correlation always proves the reverse causal direction', 'Two increasing variables cannot be correlated', 'Seasonal data are always invalid'], 'A lurking variable such as warm weather can drive both. Association alone does not identify a causal mechanism.')]
}

SUBJECTS = ['AP Calculus AB', 'AP Calculus BC', *BANK]


def build_quiz(subject, count, topic='All topics'):
    pool = question_bank(subject)
    if topic != 'All topics':
        pool = [item for item in pool if item['topic'] == topic]
    if count not in {5, 10, 20} or count > len(pool):
        raise ValueError('Choose a length that fits the available questions.')
    rng = random.SystemRandom()
    result = []
    for item in rng.sample(pool, count):
        order = list(range(4))
        rng.shuffle(order)
        result.append({**item, 'options': [item['options'][i] for i in order], 'correct': order.index(item['correct'])})
    return result

import streamlit as st
import random
import pandas as pd
import time
from collections import defaultdict

# Set page config
st.set_page_config(
    page_title="Copa Libertadores 2025 Draw Simulator",
    page_icon="lib_logo.png",
    layout="wide"
)

# Language dictionaries for translations
TRANSLATIONS = {
    "en": {
        "l_flag": "🇬🇧",
        "name": "English",
        "page_title": "Copa Libertadores 2025 Group Stage Draw Simulator",
        "intro": "This application simulates the group stage draw for the Copa Libertadores 2025 tournament.",
        "rules_title": "Rules:",
        "rule1": "32 teams are divided into 8 groups (A-H)",
        "rule2": "Each group has one team from each of the four pots",
        "rule3": "Teams from the same country can't be drawn into the same group",
        "rule4": "**Exception:** Third stage winners are exempt from the country restriction",
        "rule5": "Botafogo (current champion) will always be placed in Group A",
        "controls": "Controls",
        "animation_speed": "Animation Speed",
        "run_simulation": "Run Simulation",
        "skip_animation": "Skip Animation",
        "clear_results": "Clear Results",
        "drawing": "Drawing:",
        "draw_complete": "Draw Complete! All teams have been assigned to their groups.",
        "team_pots": "Team Pots",
        "team": "Team",
        "flag": "Flag",
        "country": "Country",
        "rank": "CONMEBOL Ranking",
        "draw_results": "Draw Results",
        "all_groups": "All Groups Overview",
        "group": "Group",
        "pot": "Pot",
        "language": "Language"
    },
    "es": {
        "l_flag": "🇪🇸",
        "name": "Español",
        "page_title": "Simulador del Sorteo de Fase de Grupos de la Copa Libertadores 2025",
        "intro": "Esta aplicación simula el sorteo de la fase de grupos del torneo Copa Libertadores 2025.",
        "rules_title": "Reglas:",
        "rule1": "32 equipos divididos en 8 grupos (A-H)",
        "rule2": "Cada grupo tiene un equipo de cada uno de los cuatro bombos",
        "rule3": "Equipos del mismo país no pueden estar en el mismo grupo",
        "rule4": "**Excepción:** Los ganadores de la tercera fase están exentos de la restricción por país",
        "rule5": "Botafogo (campeón actual) siempre estará ubicado en el Grupo A",
        "controls": "Controles",
        "animation_speed": "Velocidad de Animación",
        "run_simulation": "Simular",
        "skip_animation": "Saltar Animación",
        "clear_results": "Borrar Resultados",
        "drawing": "Sorteando:",
        "draw_complete": "¡Sorteo Completo! Todos los equipos han sido asignados a sus grupos.",
        "team_pots": "Bombos de Equipos",
        "team": "Equipo",
        "flag": "Bandera",
        "country": "País",
        "rank": "Ranking CONMEBOL",
        "draw_results": "Resultados del Sorteo",
        "all_groups": "Vista General de Todos los Grupos",
        "group": "Grupo",
        "pot": "Bombo",
        "language": "Idioma"
    },
    "pt": {
        "l_flag": "🇧🇷",
        "name": "Português",
        "page_title": "Simulador do Sorteio da Fase de Grupos da Copa Libertadores 2025",
        "intro": "Esta aplicação simula o sorteio da fase de grupos do torneio Copa Libertadores 2025.",
        "rules_title": "Regras:",
        "rule1": "32 equipes divididas em 8 grupos (A-H)",
        "rule2": "Cada grupo possui uma equipe de cada um dos quatro potes",
        "rule3": "Equipes do mesmo país não podem ser sorteadas para o mesmo grupo",
        "rule4": "**Exceção:** Vencedores da terceira fase estão isentos da restrição por país",
        "rule5": "Botafogo (atual campeão) sempre será colocado no Grupo A",
        "controls": "Controles",
        "animation_speed": "Velocidade da Animação",
        "run_simulation": "Iniciar Simulação",
        "skip_animation": "Pular Animação",
        "clear_results": "Limpar Resultados",
        "drawing": "Sorteando:",
        "draw_complete": "Sorteio Concluído! Todas as equipes foram designadas para seus grupos.",
        "team_pots": "Potes de Equipes",
        "team": "Equipe",
        "flag": "Bandeira",
        "country": "País",
        "rank": "Ranking CONMEBOL",
        "draw_results": "Resultados do Sorteio",
        "all_groups": "Visão Geral de Todos os Grupos",
        "group": "Grupo",
        "pot": "Pote",
        "language": "Idioma"
    }
}

# Language options for the dropdown
LANGUAGE_OPTIONS = {
    "en": f"{TRANSLATIONS['en']['l_flag']} English",
    "es": f"{TRANSLATIONS['es']['l_flag']} Español",
    "pt": f"{TRANSLATIONS['pt']['l_flag']} Português"
}

# Teams data - updated with actual 2025 participants
TEAMS = {
    "Pot 1": [
        {"name": "Botafogo", "country": "🇧🇷 Brazil", "flag": "🇧🇷", "rank": "21", "fixed_group": "A"},
        {"name": "River Plate", "country": "🇦🇷 Argentina", "flag": "🇦🇷", "rank": "1"},
        {"name": "Palmeiras", "country": "🇧🇷 Brazil", "flag": "🇧🇷", "rank": "2"},
        {"name": "Flamengo", "country": "🇧🇷 Brazil", "flag": "🇧🇷", "rank": "4"},
        {"name": "Peñarol", "country": "🇺🇾 Uruguay", "flag": "🇺🇾", "rank": "5"},
        {"name": "Nacional", "country": "🇺🇾 Uruguay", "flag": "🇺🇾", "rank": "6"},
        {"name": "São Paulo", "country": "🇧🇷 Brazil", "flag": "🇧🇷", "rank": "8"},
        {"name": "Racing", "country": "🇦🇷 Argentina", "flag": "🇦🇷", "rank": "12"}
    ],
    "Pot 2": [
        {"name": "Olimpia", "country": "🇵🇾 Paraguay", "flag": "🇵🇾", "rank": "13"},
        {"name": "LDU Quito", "country": "🇪🇨 Ecuador", "flag": "🇪🇨", "rank": "14"},
        {"name": "Internacional", "country": "🇧🇷 Brazil", "flag": "🇧🇷", "rank": "15"},
        {"name": "Libertad", "country": "🇵🇾 Paraguay", "flag": "🇵🇾", "rank": "16"},
        {"name": "Independiente del Valle", "country": "🇪🇨 Ecuador", "flag": "🇪🇨", "rank": "17"},
        {"name": "Colo-Colo", "country": "🇨🇱 Chile", "flag": "🇨🇱", "rank": "23"},
        {"name": "Estudiantes", "country": "🇦🇷 Argentina", "flag": "🇦🇷", "rank": "24"},
        {"name": "Bolívar", "country": "🇧🇴 Bolivia", "flag": "🇧🇴", "rank": "27"}
    ],
    "Pot 3": [
        {"name": "Atlético Nacional", "country": "🇨🇴 Colombia", "flag": "🇨🇴", "rank": "28"},
        {"name": "Vélez Sarsfield", "country": "🇦🇷 Argentina", "flag": "🇦🇷", "rank": "29"},
        {"name": "Fortaleza", "country": "🇧🇷 Brazil", "flag": "🇧🇷", "rank": "37"},
        {"name": "Sporting Cristal", "country": "🇵🇪 Peru", "flag": "🇵🇪", "rank": "38"},
        {"name": "Universitario", "country": "🇵🇪 Peru", "flag": "🇵🇪", "rank": "41"},
        {"name": "Talleres", "country": "🇦🇷 Argentina", "flag": "🇦🇷", "rank": "46"},
        {"name": "Deportivo Táchira", "country": "🇻🇪 Venezuela", "flag": "🇻🇪", "rank": "49"},
        {"name": "Universidad de Chile", "country": "🇨🇱 Chile", "flag": "🇨🇱", "rank": "57"}
    ],
    "Pot 4": [
        {"name": "Carabobo", "country": "🇻🇪 Venezuela", "flag": "🇻🇪", "rank": "173"},
        {"name": "Atlético Bucaramanga", "country": "🇨🇴 Colombia", "flag": "🇨🇴", "rank": "198"},
        {"name": "San Antonio Bulo Bulo", "country": "🇧🇴 Bolivia", "flag": "🇧🇴", "rank": "0"},
        {"name": "Central Córdoba", "country": "🇦🇷 Argentina", "flag": "🇦🇷", "rank": "0"},
        {"name": "Alianza Lima", "country": "🇵🇪 Peru", "flag": "🇵🇪", "rank": "50", "is_qualifier": True},
        {"name": "Bahia", "country": "🇧🇷 Brazil", "flag": "🇧🇷", "rank": "77", "is_qualifier": True},
        {"name": "Cerro Porteño", "country": "🇵🇾 Paraguay", "flag": "🇵🇾", "rank": "20", "is_qualifier": True},
        {"name": "Barcelona SC", "country": "🇪🇨 Ecuador", "flag": "🇪🇨", "rank": "25", "is_qualifier": True}
    ]
}

# Initialize session state for language if not already set
if "language" not in st.session_state:
    st.session_state.language = "es"

def check_same_country(group, new_team):
    """Check if there are teams from the same country in the group"""
    # For third stage winners, we ignore the country restriction
    if new_team.get("is_qualifier", False):
        return True
        
    country_count = defaultdict(int)
    
    # Count countries in current group
    for team in group:
        # Skip third stage winners when counting countries
        if team.get("is_qualifier", False):
            continue
        country_count[team["country"]] += 1
    
    # Check if adding new team would violate rules
    if country_count[new_team["country"]] > 0:
        return False
            
    return True

def prepare_draw():
    """Prepare the draw sequence but don't execute it yet"""
    groups = {f"Group {chr(65+i)}": [] for i in range(8)}  # Groups A through H
    draw_sequence = []
    
    # First, place Botafogo in Group A
    botafogo = next(team for team in TEAMS["Pot 1"] if team["name"] == "Botafogo")
    groups["Group A"].append(botafogo)
    draw_sequence.append(("Group A", "Pot 1", botafogo))
    
    # For each pot
    for pot_name, pot_teams in TEAMS.items():
        # Skip Botafogo in Pot 1
        available_teams = [team for team in pot_teams if team.get("fixed_group") != "A"] if pot_name == "Pot 1" else pot_teams.copy()
        
        # For each group
        for group_name in groups.keys():
            # Skip Group A for Pot 1 as Botafogo is already there
            if pot_name == "Pot 1" and group_name == "Group A":
                continue
                
            while not available_teams:
                return None, None  # Indicate that we need to retry
                
            # Try to find a team that fits the group
            viable_teams = []
            
            # Check which teams can go into this group
            for team in available_teams:
                if check_same_country(groups[group_name], team):
                    viable_teams.append(team)
            
            if viable_teams:
                # Randomly select one of the viable teams
                selected_team = random.choice(viable_teams)
                groups[group_name].append(selected_team)
                available_teams.remove(selected_team)
                draw_sequence.append((group_name, pot_name, selected_team))
            else:
                # If we get here, we need to restart the draw
                return None, None
                
    return groups, draw_sequence

def run_draw(animation_speed, skip_animation):
    """Perform the draw with animation"""
    # Initialize progress containers
    if "draw_progress" not in st.session_state:
        st.session_state.draw_progress = 0
        st.session_state.current_draw = None
        st.session_state.current_groups = {f"Group {chr(65+i)}": [] for i in range(8)}

    # If we're starting a new draw
    if st.session_state.draw_progress == 0:
        # Prepare all the draw steps in advance
        prepared_groups, prepared_sequence = None, None
        while prepared_groups is None:
            prepared_groups, prepared_sequence = prepare_draw()
        
        st.session_state.final_groups = prepared_groups
        st.session_state.draw_sequence = prepared_sequence
        st.session_state.total_steps = len(prepared_sequence)
    
    # If we're skipping the animation, set progress to the end
    if skip_animation:
        st.session_state.draw_progress = st.session_state.total_steps
        st.session_state.current_groups = st.session_state.final_groups
        st.session_state.animation_complete = True
        return st.session_state.final_groups
    
    # If animation is in progress but not complete
    if st.session_state.draw_progress < st.session_state.total_steps:
        # Get the current draw step
        group_name, pot_name, team = st.session_state.draw_sequence[st.session_state.draw_progress]
        
        # Update the current draw information for display
        st.session_state.current_draw = {
            "group": group_name,
            "pot": pot_name,
            "team": team
        }
        
        # Update the current group state
        if group_name not in st.session_state.current_groups:
            st.session_state.current_groups[group_name] = []
        st.session_state.current_groups[group_name].append(team)
        
        # Increment progress
        st.session_state.draw_progress += 1
        
        # Schedule next update if not complete
        if st.session_state.draw_progress < st.session_state.total_steps:
            time.sleep(animation_speed)  # Add delay
            st.rerun()  # Modern replacement for experimental_rerun
        else:
            # Animation is complete
            st.session_state.animation_complete = True
            # This is critical - force a final rerun to update the UI with the last team
            time.sleep(animation_speed)
            st.rerun()
    
    return st.session_state.current_groups

def main():
    # Get current language translations
    lang = st.session_state.language
    t = TRANSLATIONS[lang]
    
    # Add language selector in the header
    st.markdown(
        """
        <style>
        .language-selector {
            position: absolute;
            top: 0.5rem;
            right: 1rem;
            z-index: 1000;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )
    
    with st.container():
        # Title with language selector on the right
        title_col, lang_col = st.columns([5, 1])
        
        with title_col:
            st.image("lib_logo.png", width=100)
            st.title(f"{t['page_title']}")
            
        with lang_col:
            # Map language codes to their display names with flags
            language_display = {
                "en": f"{TRANSLATIONS['en']['l_flag']} English",
                "es": f"{TRANSLATIONS['es']['l_flag']} Español",
                "pt": f"{TRANSLATIONS['pt']['l_flag']} Português"
            }
            
            # Create a mapping between the display strings and the language codes
            display_to_code = {display: code for code, display in language_display.items()}
            
            # Show the dropdown with the full language names
            selected_display = st.selectbox(
                f"🌎 {t['language']}",
                options=list(language_display.values()),
                index=list(language_display.values()).index(language_display[lang]),
                key="language_selector"
            )
            
            # Get the corresponding language code
            selected_lang = display_to_code[selected_display]
            
            # Change language if selection changed
            if selected_lang != lang:
                st.session_state.language = selected_lang
                st.rerun()
    
    st.markdown(f"""
    {t['intro']}
    
    ### {t['rules_title']}
    - {t['rule1']}
    - {t['rule2']}
    - {t['rule3']}
    - {t['rule4']}
    - {t['rule5']}
    """)
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader(t['controls'])
        
        # Animation speed control
        animation_speed = st.select_slider(
            t['animation_speed'],
            options=[0.5, 1.0, 1.5, 2.0],
            value=1.0,
            format_func=lambda x: f"{x}s"
        )
        
        # Draw button row
        button_col1, button_col2 = st.columns(2)
        
        with button_col1:
            if st.button(t['run_simulation'], type="primary"):
                # Reset the draw state
                st.session_state.draw_progress = 0
                st.session_state.current_groups = {f"Group {chr(65+i)}": [] for i in range(8)}
                st.session_state.show_results = True
                st.session_state.animation_complete = False
                
                # Start the draw with animation
                run_draw(animation_speed, False)
        
        with button_col2:
            if st.button(t['skip_animation']):
                # Reset the draw state
                st.session_state.draw_progress = 0
                st.session_state.current_groups = {f"Group {chr(65+i)}": [] for i in range(8)}
                st.session_state.show_results = True
                
                # Run the draw immediately without animation
                groups = run_draw(animation_speed, True)
                if groups:
                    st.session_state.groups = groups
        
        if st.button(t['clear_results']):
            # Reset all relevant session state variables
            st.session_state.show_results = False
            st.session_state.draw_progress = 0
            st.session_state.current_groups = {f"Group {chr(65+i)}": [] for i in range(8)}
            st.session_state.animation_complete = False
            # Make sure to also clear the current_draw to avoid lingering references
            st.session_state.current_draw = None
            
        # Draw progress indicator
        if st.session_state.get("show_results", False) and st.session_state.get("draw_progress", 0) > 0:
            progress_percentage = st.session_state.draw_progress / st.session_state.get("total_steps", 1)
            st.progress(progress_percentage)
            
            # Show current draw info if animation is in progress
            if st.session_state.get("current_draw") and not st.session_state.get("animation_complete", False):
                current = st.session_state.current_draw
                st.info(f"**{t['drawing']}** {current['team']['flag']} {current['team']['name']} → {current['group']}")
            elif st.session_state.get("animation_complete", False):
                st.success(f"**{t['draw_complete']}**")
            
        # Team pots display
        st.subheader(t['team_pots'])
        pot_tabs = st.tabs(["Pot 1", "Pot 2", "Pot 3", "Pot 4"])
        
        for i, (pot_name, pot_tab) in enumerate(zip(TEAMS.keys(), pot_tabs)):
            with pot_tab:
                pot_df = pd.DataFrame(TEAMS[pot_name])
                display_cols = ["name", "country", "rank"]
                st.dataframe(
                    pot_df[display_cols],
                    column_config={
                        "name": t['team'],
                        "country": t['country'],
                        "rank": t['rank']
                    },
                    hide_index=True
                )
    
    with col2:
        st.subheader(t['draw_results'])
        
        if st.session_state.get("show_results", False):
            current_groups = st.session_state.get("current_groups", {})
            
            tabs = st.tabs([group_name for group_name in current_groups.keys()])
            
            for group_name, tab in zip(current_groups.keys(), tabs):
                with tab:
                    group_data = []
                    for i, team in enumerate(current_groups.get(group_name, [])):
                        # Determine if this is the most recently drawn team
                        is_latest = False
                        if (st.session_state.get("current_draw") and 
                            st.session_state.get("current_draw")["group"] == group_name and
                            st.session_state.get("current_draw")["team"] == team and
                            not st.session_state.get("animation_complete", False)):
                            is_latest = True
                            
                        pot_num = i + 1
                        group_data.append({
                            "Pot": f"{t['pot']} {pot_num}",
                            "Team": team["name"],
                            "Country": team["country"],
                            "Rank": team["rank"],
                        })
                    
                    if group_data:
                        group_df = pd.DataFrame(group_data)
                        st.dataframe(
                            group_df,
                            column_config={
                                "Pot": t['pot'],
                                "Team": t['team'],
                                "Country": t['country'],
                                "Rank": t['rank'],
                            },
                            hide_index=True
                        )
            
            # Show all groups in a single table view
            st.subheader(t['all_groups'])
            
            all_groups_data = []
            for group_name, group_teams in current_groups.items():
                group_dict = {t['group']: group_name}
                
                for i, team in enumerate(group_teams):
                    pot_key = f"{t['pot']} {i+1}"
                    team_rank = f"({team['rank']})"
                    
                    # Highlight the most recently drawn team
                    is_latest = False
                    if (st.session_state.get("current_draw") and 
                        st.session_state.get("current_draw")["group"] == group_name and
                        st.session_state.get("current_draw")["team"] == team and
                        not st.session_state.get("animation_complete", False)):
                        group_dict[pot_key] = f"✨ {team['flag']} {team['name']}"
                    else:
                        group_dict[pot_key] = f"{team['flag']} {team['name']}"
                
                all_groups_data.append(group_dict)
            
            all_groups_df = pd.DataFrame(all_groups_data)
            
            # Get column names based on current language
            column_config = {
                t['group']: t['group'],
                f"{t['pot']} 1": f"{t['pot']} 1",
                f"{t['pot']} 2": f"{t['pot']} 2",
                f"{t['pot']} 3": f"{t['pot']} 3",
                f"{t['pot']} 4": f"{t['pot']} 4"
            }
            
            st.dataframe(
                all_groups_df,
                column_config=column_config,
                hide_index=True
            )
            
            # Continue animation if in progress
            if (st.session_state.get("draw_progress", 0) < st.session_state.get("total_steps", 0) and 
                st.session_state.get("show_results", False) and
                not st.session_state.get("animation_complete", False)):
                run_draw(animation_speed, False)

# Initialize session state if not already done
if "show_results" not in st.session_state:
    st.session_state.show_results = False
if "groups" not in st.session_state:
    st.session_state.groups = None
if "draw_progress" not in st.session_state:
    st.session_state.draw_progress = 0
if "current_groups" not in st.session_state:
    st.session_state.current_groups = {f"Group {chr(65+i)}": [] for i in range(8)}
if "animation_complete" not in st.session_state:
    st.session_state.animation_complete = False

if __name__ == "__main__":
    main()
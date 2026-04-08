package main

import (
	"fmt"
	"os"
	"strings"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

// --- Theme ---

var (
	base     = lipgloss.NewStyle().Foreground(lipgloss.Color("252"))
	muted    = lipgloss.NewStyle().Foreground(lipgloss.Color("243"))
	accent   = lipgloss.NewStyle().Foreground(lipgloss.Color("86"))
	bold     = lipgloss.NewStyle().Bold(true)
	dim      = lipgloss.NewStyle().Foreground(lipgloss.Color("243"))
	success  = lipgloss.NewStyle().Foreground(lipgloss.Color("78"))
	errorRed = lipgloss.NewStyle().Foreground(lipgloss.Color("203"))

	borderStyle = lipgloss.NewStyle().
			BorderStyle(lipgloss.RoundedBorder()).
			BorderForeground(lipgloss.Color("243")).
			Padding(1, 2)

	activeBorder = borderStyle.
			BorderForeground(lipgloss.Color("86"))
)

// --- Messages ---

type errMsg struct{ err error }

// --- Model ---

type Model struct {
	width  int
	height int
	items  []string
	cursor int
}

func newModel() Model {
	return Model{
		items: []string{
			"Dashboard",
			"Records",
			"Logs",
			"Settings",
		},
	}
}

func (m Model) Init() tea.Cmd {
	return nil
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.WindowSizeMsg:
		m.width = msg.Width
		m.height = msg.Height
		return m, nil

	case tea.KeyMsg:
		switch msg.String() {
		case "q", "ctrl+c":
			return m, tea.Quit
		case "up", "k":
			if m.cursor > 0 {
				m.cursor--
			}
		case "down", "j":
			if m.cursor < len(m.items)-1 {
				m.cursor++
			}
		case "enter":
			// Handle selection
			return m, nil
		case "?":
			// Toggle help
			return m, nil
		}
	}

	return m, nil
}

func (m Model) View() string {
	if m.width < 50 || m.height < 15 {
		return errorRed.Render("Terminal too small. Please resize to at least 50x15.")
	}

	// Sidebar
	sidebarWidth := 22
	var sidebarItems strings.Builder
	for i, item := range m.items {
		cursor := " "
		style := base
		if i == m.cursor {
			cursor = accent.Render("▸")
			style = bold.Foreground(lipgloss.Color("86"))
		}
		fmt.Fprintf(&sidebarItems, " %s %s\n", cursor, style.Render(item))
	}

	sidebar := borderStyle.
		Width(sidebarWidth - 4).
		Render(
			bold.Render("NAVIGATION") + "\n\n" + sidebarItems.String(),
		)

	// Content
	contentWidth := m.width - sidebarWidth - 4
	content := activeBorder.
		Width(contentWidth - 4).
		Height(m.height - 6).
		Render(
			bold.Render("Welcome") + "\n\n" +
				muted.Render("Select an item from the sidebar or press ? for help."),
		)

	// Layout
	body := lipgloss.JoinHorizontal(lipgloss.Top, sidebar, content)

	// Status bar
	statusBar := lipgloss.NewStyle().
		Width(m.width).
		Background(lipgloss.Color("236")).
		Foreground(lipgloss.Color("252")).
		Padding(0, 2).
		Render(
			success.Render("● Connected") +
				"  " + muted.Render("j/k: navigate  Enter: select  ?: help  q: quit"),
		)

	return lipgloss.JoinVertical(lipgloss.Left, body, statusBar)
}

// --- Entry ---

func main() {
	p := tea.NewProgram(
		newModel(),
		tea.WithAltScreen(),
		tea.WithMouseCellMotion(),
	)

	if _, err := p.Run(); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}
}

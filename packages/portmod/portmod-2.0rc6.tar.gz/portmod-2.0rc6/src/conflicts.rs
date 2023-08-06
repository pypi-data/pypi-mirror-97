use crossterm::{
    event::{self, DisableMouseCapture, EnableMouseCapture, Event as CEvent, KeyCode},
    execute,
    terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen},
};
use std::collections::{HashMap, HashSet};
use std::io;
use std::sync::mpsc;
use std::thread;
use std::time::Duration;
use tui::backend::CrosstermBackend;
use tui::layout::{Constraint, Direction, Layout};
use tui::style::{Color, Modifier, Style};
use tui::text::Span;
use tui::widgets::{Block, Borders, List, ListItem, ListState};
use tui::Terminal;

enum Event<I> {
    Input(I),
    Tick,
}

fn get_conflicts(base_index: usize, entries: &[(String, HashSet<String>)]) -> Vec<String> {
    let mut conflicts = vec![];
    for (index, (other_key, other_entries)) in entries.iter().enumerate() {
        if index != base_index {
            let intersection = other_entries & &entries[base_index].1;
            let mut cur_conflicts: Vec<&String> = intersection.iter().collect();
            cur_conflicts.sort();
            if !cur_conflicts.is_empty() {
                if base_index > index {
                    conflicts.push(format!("Higher - {}:\n", other_key));
                } else {
                    conflicts.push(format!("Lower - {}:\n", other_key));
                }
                for file in cur_conflicts {
                    conflicts.push(format!("    {}", file));
                }
            }
        }
    }
    conflicts
}

pub fn conflicts(
    left_title: &str,
    right_title: &str,
    entries: &[(String, HashSet<String>)],
) -> Result<(), io::Error> {
    // Initialize Terminal
    enable_raw_mode().unwrap();
    let mut stdout = std::io::stdout();
    execute!(stdout, EnterAlternateScreen, EnableMouseCapture).unwrap();
    let backend = CrosstermBackend::new(stdout);
    let mut terminal = Terminal::new(backend)?;
    terminal.hide_cursor()?;

    let keys: Vec<&String> = entries.iter().map(|(x, _)| x).collect();

    let (tx, rx) = mpsc::channel();
    {
        thread::spawn(move || {
            let mut last_tick = std::time::Instant::now();
            let tick_rate = Duration::from_millis(1000);
            loop {
                // poll for tick rate duration, if no events, sent tick event.
                if event::poll(tick_rate - last_tick.elapsed()).unwrap() {
                    if let CEvent::Key(key) = event::read().unwrap() {
                        tx.send(Event::Input(key)).unwrap();
                    }
                }
                if last_tick.elapsed() >= tick_rate {
                    tx.send(Event::Tick).unwrap();
                    last_tick = std::time::Instant::now();
                }
            }
        });
    }

    terminal.clear()?;
    let mut cache: HashMap<usize, Vec<String>> = HashMap::new();

    fn move_up(start: usize, amount: usize, max: usize) -> usize {
        if start >= amount {
            start - amount
        } else if start == max - 1 && max < amount {
            0
        } else {
            max - 1
        }
    }

    fn move_down(start: usize, amount: usize, max: usize) -> usize {
        if start == 0 && max < amount {
            max - 1
        } else if start + amount > max - 1 {
            0
        } else {
            start + amount
        }
    }

    let mut left_state = ListState::default();
    let mut right_state = ListState::default();
    left_state.select(Some(0));

    loop {
        terminal.draw(|f| {
            let chunks = Layout::default()
                .direction(Direction::Horizontal)
                .margin(1)
                .constraints([Constraint::Percentage(50), Constraint::Percentage(50)].as_ref())
                .split(f.size());

            let style = Style::default().fg(Color::White).bg(Color::Black);
            let left_items: Vec<ListItem> =
                keys.iter().map(|i| ListItem::new(Span::raw(*i))).collect();
            let left_list = List::new(left_items)
                .block(Block::default().borders(Borders::ALL).title(left_title))
                .style(style)
                .highlight_style(style.fg(Color::LightGreen).add_modifier(Modifier::BOLD))
                .highlight_symbol(">");
            cache
                .entry(left_state.selected().unwrap())
                .or_insert_with(|| get_conflicts(left_state.selected().unwrap(), entries));
            let right_items: Vec<ListItem> = cache
                .get(&left_state.selected().unwrap())
                .unwrap()
                .iter()
                .map(|x| ListItem::new(Span::raw(x)))
                .collect();
            let right_list = List::new(right_items)
                .block(Block::default().borders(Borders::ALL).title(right_title))
                .style(style)
                .highlight_style(style.fg(Color::LightGreen).add_modifier(Modifier::BOLD))
                .highlight_symbol(">");
            f.render_stateful_widget(right_list, chunks[1], &mut right_state);
            f.render_stateful_widget(left_list, chunks[0], &mut left_state);
        })?;
        let selected_left = left_state.selected().unwrap();
        match rx.recv() {
            Ok(Event::Input(event)) => match event.code {
                KeyCode::Esc | KeyCode::Char('q') => {
                    disable_raw_mode().unwrap();
                    execute!(
                        terminal.backend_mut(),
                        LeaveAlternateScreen,
                        DisableMouseCapture
                    )
                    .unwrap();
                    terminal.show_cursor()?;
                    break;
                }
                KeyCode::Left | KeyCode::Char('a') | KeyCode::Char('h') => {
                    right_state.select(None);
                }
                KeyCode::Down | KeyCode::Char('s') | KeyCode::Char('j') => {
                    if let Some(selected) = right_state.selected() {
                        right_state.select(Some(move_down(
                            selected,
                            1,
                            cache.get(&selected_left).unwrap().len(),
                        )));
                    } else {
                        left_state.select(Some(move_down(selected_left, 1, keys.len())));
                    }
                }
                KeyCode::Right | KeyCode::Char('d') | KeyCode::Char('l') => {
                    right_state.select(Some(0));
                }
                KeyCode::Up | KeyCode::Char('w') | KeyCode::Char('k') => {
                    if let Some(selected) = right_state.selected() {
                        right_state.select(Some(move_up(
                            selected,
                            1,
                            cache.get(&selected_left).unwrap().len(),
                        )));
                    } else {
                        left_state.select(Some(move_up(selected_left, 1, keys.len())));
                    }
                }
                KeyCode::PageUp => {
                    let term_height = terminal.size()?.height;
                    if let Some(selected) = right_state.selected() {
                        right_state.select(Some(move_up(
                            selected,
                            (term_height / 2) as usize,
                            cache.get(&selected_left).unwrap().len(),
                        )));
                    } else {
                        left_state.select(Some(move_up(
                            selected_left,
                            (term_height / 2) as usize,
                            keys.len(),
                        )));
                    }
                }
                KeyCode::PageDown => {
                    let term_height = terminal.size()?.height;
                    if let Some(selected) = right_state.selected() {
                        right_state.select(Some(move_down(
                            selected,
                            (term_height / 2) as usize,
                            cache.get(&selected_left).unwrap().len(),
                        )));
                    } else {
                        left_state.select(Some(move_down(
                            selected_left,
                            (term_height / 2) as usize,
                            keys.len(),
                        )));
                    }
                }
                _ => {}
            },
            Ok(Event::Tick) => {}
            Err(e) => {
                panic!("{:?}", e);
            }
        }
    }

    Ok(())
}

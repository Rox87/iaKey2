use rdev::{listen, Event, EventType, Key};

fn main() {
    println!("Listener ativo. Pressione F2 (melhore) ou F8 (general) ou F9 (python) ou F10(html) para enviar consulta o Gemini.");

    if let Err(error) = listen(callback) {
        eprintln!("Error: {:?}", error);
    }
}

fn callback(event: Event) {
    if let EventType::KeyPress(key) = event.event_type {
        match key {
            Key::F2 => on_activate_melhore(),
            Key::F8 => on_activate_general(),
            Key::F9 => on_activate_python(),
            Key::F10 => on_activate_html(),
            _ => {}
        }
    }
}

fn on_activate_melhore() {
    println!("Ação F2: melhore");
}

fn on_activate_general() {
    println!("Ação F8: general");
}

fn on_activate_python() {
    println!("Ação F9: python");
}

fn on_activate_html() {
    println!("Ação F10: html");
}

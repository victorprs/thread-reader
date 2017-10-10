#[macro_use]
extern crate serde_derive;

extern crate serde;

extern crate serde_json;

use std::env;
use std::fs::File;
use std::io::prelude::*;

#[derive(Serialize, Deserialize, Debug)]
struct Secret {
	key: String,
	secret: String,
}

fn main() {
	let mut filename = env::current_dir().unwrap();
	filename.push("secret.json");
	let mut f = File::open(filename)
		.expect("file not found");
	let mut contents = String::new();
	f.read_to_string(&mut contents).unwrap();

	let secret: Secret = serde_json::from_str(&contents).unwrap();
	println!("Secret: {}", secret.key);

}

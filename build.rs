use std::io::Result;

fn main() -> Result<()> {
    prost_build::compile_protos(&["proto/stored_document.proto"], &["proto/"])?;
    Ok(())
}

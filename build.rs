use std::io::Result;

fn main() -> Result<()> {
    let file_descriptors = protox::compile(["proto/stored_document.proto"], ["proto/"]).unwrap();
    prost_build::compile_fds(file_descriptors).unwrap();
    Ok(())
}

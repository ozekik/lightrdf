#[macro_export]
macro_rules! gen_create_iter {
    ($error:ident) => {
        fn create_iter<P: TriplesParser<Error = $error>>(
            parser: P,
        ) -> impl iter::Iterator<Item = Result<common::StringTriple, common::ParserError>> {
            let mut it = parser.into_iter(move |t| {
                let st = common::triple_to_striple(t);
                Ok(st) as Result<_, common::ParserError>
            });
            iter::from_fn(move || match it.next() {
                Some(Ok(v)) => Some(Ok(v)),
                Some(Err(e)) => Some(Err(e)),
                _ => None,
            })
        }
    };
}

"""The nox file for the project."""

import nox


@nox.session
def tests(session: nox.Session) -> None:
    """Run the unit and regular tests."""
    session.install(".[test]")
    session.run("pytest", *session.posargs)


@nox.session
def docs(session: nox.Session) -> None:
    """Build the docs. Pass "--serve" to serve."""
    session.install(".[docs]")
    session.chdir("docs")
    session.run("sphinx-build", "-M", "html", ".", "build")


@nox.session
def serve(session: nox.Session) -> None:
    """Serves the documentation."""
    docs(session)
    session.run("python", "-m", "http.server", "8000", "-d", "_build/html")

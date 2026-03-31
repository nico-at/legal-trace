from ris_client.enums import APPLICATION_CONTROLLER, Application


def test_every_application_has_a_controller():
    """Missing entry raises KeyError at runtime in search()."""
    for app in Application:
        assert app in APPLICATION_CONTROLLER, f"Application.{app.name} has no controller"

import logging

import responses

from orthanc_ext import event_dispatcher
from orthanc_ext.orthanc import OrthancApiHandler
from orthanc_ext.orthanc_utilities import get_metadata_of_first_instance_of_series
from orthanc_ext.scripts.auto_forward import forward_dicom, DicomReceivedMatcher

orthanc = OrthancApiHandler()
session = event_dispatcher.create_internal_requests_session('https://localhost:8042', '')


@responses.activate
def test_autoforward_on_match_shall_start_start_modality_store(caplog):
    caplog.set_level(logging.INFO)
    responses.add(responses.POST, 'https://localhost:8042/modalities/pacs/store', body="study-uuid", status=200)

    register_and_trigger_handler([DicomReceivedMatcher(lambda uid, _: True, lambda uid, _: 'pacs')])

    assert caplog.messages == ["DICOM export to modality 'pacs' started for resource 'study-uuid'"]


def is_not_dicom_origin(resource_id, session):
    return get_metadata_of_first_instance_of_series(session, resource_id, 'Origin') != 'DicomProtocol'


@responses.activate
def test_autoforward_on_multiple_matches_shall_start_start_modality_store(caplog):
    caplog.set_level(logging.INFO)
    responses.add(responses.GET, 'https://localhost:8042/series/study-uuid/instances',
                  json=[{'ID': "b99cd218-ae67f0d7-70324b6b-2b095801-f858dedf"}])
    responses.add(responses.GET,
                  'https://localhost:8042/instances/b99cd218-ae67f0d7-70324b6b-2b095801-f858dedf/metadata/Origin',
                  body='Plugins')
    responses.add(responses.POST, 'https://localhost:8042/modalities/pacs1/store', body="study-uuid", status=200)
    responses.add(responses.POST, 'https://localhost:8042/modalities/pacs2/store', body="study-uuid", status=200)

    matcher1 = DicomReceivedMatcher(is_not_dicom_origin, lambda uid, _: 'pacs1')
    matcher2 = DicomReceivedMatcher(lambda uid, _: True, lambda uid, _: 'pacs2')

    register_and_trigger_handler([matcher1, matcher2])

    assert caplog.messages == ["DICOM export to modality 'pacs1' started for resource 'study-uuid'",
                               "DICOM export to modality 'pacs2' started for resource 'study-uuid'"]


def register_and_trigger_handler(matchers):
    event_dispatcher.register_event_handlers(
        {
            orthanc.ChangeType.STABLE_STUDY: forward_dicom(matchers)
        }, orthanc_module=orthanc, requests_session=session)
    orthanc.on_change(orthanc.ChangeType.STABLE_STUDY, '', 'study-uuid')


def test_autoforward_on_no_match_shall_log_and_continue(caplog):
    register_and_trigger_handler([DicomReceivedMatcher(lambda uid, _: False, lambda uid, _: 'pacs')])

    message, = caplog.messages
    assert "did not match; resource 'study-uuid' not forwarded" in message

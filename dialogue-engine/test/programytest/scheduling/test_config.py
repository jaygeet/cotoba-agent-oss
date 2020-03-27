"""
Copyright (c) 2020 COTOBA DESIGN, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import unittest

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.scheduling.config import SchedulerConfiguration
from programy.clients.events.console.config import ConsoleConfiguration


class SchedulerConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
          scheduler:
            name: Scheduler1
            debug_level: 0
            add_listeners: True
            remove_all_jobs: True

            jobstore:
                name:   mongo

                mongo:
                    collection: example_jobs

                redis:
                    jobs_key: example.jobs
                    run_times_key: example.run_times

                sqlalchemy:
                    url: sqlite:///jobs.sqlite

            threadpool:
                max_workers: 20

            processpool:
                max_workers: 5

            job_defaults:
                coalesce: False
                max_instances: 3

        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("console")

        scheduler_config = SchedulerConfiguration()
        scheduler_config.load_config_section(yaml, bot_config, ".")

        self.assertEqual("Scheduler1", scheduler_config.name)
        self.assertEqual(0, scheduler_config.debug_level)
        self.assertTrue(scheduler_config.add_listeners)
        self.assertTrue(scheduler_config.remove_all_jobs)

        self.assertIsNotNone(scheduler_config.jobstore)
        self.assertIsNotNone(scheduler_config.jobstore.jobstore)
        self.assertEqual("example_jobs", scheduler_config.jobstore.jobstore.collection)

        self.assertIsNotNone(scheduler_config.threadpool)
        self.assertEqual(20, scheduler_config.threadpool.max_workers)

        self.assertIsNotNone(scheduler_config.processpool)
        self.assertEqual(5, scheduler_config.processpool.max_workers)

        self.assertIsNotNone(scheduler_config.job_defaults)
        self.assertEqual(False, scheduler_config.job_defaults.coalesce)
        self.assertEqual(3, scheduler_config.job_defaults.max_instances)

    def test_without_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
            scheduler:
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("console")

        scheduler_config = SchedulerConfiguration()
        scheduler_config.load_config_section(yaml, bot_config, ".")

        self.assertIsNone(scheduler_config.name)
        self.assertEqual(0, scheduler_config.debug_level)
        self.assertFalse(scheduler_config.add_listeners)
        self.assertFalse(scheduler_config.remove_all_jobs)

        self.assertIsNone(scheduler_config.jobstore)
        self.assertIsNone(scheduler_config.threadpool)
        self.assertIsNone(scheduler_config.processpool)
        self.assertIsNone(scheduler_config.job_defaults)

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        bot:
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("console")

        scheduler_config = SchedulerConfiguration()
        scheduler_config.load_config_section(yaml, bot_config, ".")

        self.assertIsNone(scheduler_config.name)
        self.assertEqual(0, scheduler_config.debug_level)
        self.assertFalse(scheduler_config.add_listeners)
        self.assertFalse(scheduler_config.remove_all_jobs)

        self.assertIsNone(scheduler_config.jobstore)
        self.assertIsNone(scheduler_config.threadpool)
        self.assertIsNone(scheduler_config.processpool)
        self.assertIsNone(scheduler_config.job_defaults)

    def test_create_scheduler_config_mongo(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
          scheduler:
            name: Scheduler1
            debug_level: 0
            add_listeners: True
            remove_all_jobs: True

            jobstore:
                name:   mongo

                mongo:
                    collection: example_jobs

            threadpool:
                max_workers: 20

            processpool:
                max_workers: 5

            job_defaults:
                coalesce: False
                max_instances: 3

        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("console")

        scheduler_config = SchedulerConfiguration()
        scheduler_config.load_config_section(yaml, bot_config, ".")

        config = scheduler_config.create_scheduler_config()
        self.assertIsNotNone(config)

    def test_create_scheduler_config_redis(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
          scheduler:
            name: Scheduler1
            debug_level: 0
            add_listeners: True
            remove_all_jobs: True

            jobstore:
                name:   redis

                redis:
                    jobs_key: example.jobs
                    run_times_key: example.run_times

            threadpool:
                max_workers: 20

            processpool:
                max_workers: 5

            job_defaults:
                coalesce: False
                max_instances: 3

        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("console")

        scheduler_config = SchedulerConfiguration()
        scheduler_config.load_config_section(yaml, bot_config, ".")

        config = scheduler_config.create_scheduler_config()
        self.assertIsNotNone(config)

    def test_create_scheduler_config_sqlalchemy(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
          scheduler:
            name: Scheduler1
            debug_level: 0
            add_listeners: True
            remove_all_jobs: True

            jobstore:
                name:   sqlalchemy

                sqlalchemy:
                    url: sqlite:///jobs.sqlite

            threadpool:
                max_workers: 20

            processpool:
                max_workers: 5

            job_defaults:
                coalesce: False
                max_instances: 3

        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("console")

        scheduler_config = SchedulerConfiguration()
        scheduler_config.load_config_section(yaml, bot_config, ".")

        config = scheduler_config.create_scheduler_config()
        self.assertIsNotNone(config)

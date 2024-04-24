from .java_extractor import JavaExtractor
from .java_extractor import Listener
from .grammer.JavaParser import JavaParser

def test_extract():
    extractor = JavaExtractor()
    file_content = """
    package com.example;
    import java.util.List;
    public class TestClass {
        private int number;
        public void testMethod(String param) {
            List<String> list = new ArrayList<>();
            list.add(param);
            System.out.println(list);
        }
    }
    """
    methods = ["testMethod"]
    expected_ast_info = {
        'packageName': 'com.example',
        'className': 'TestClass',
        'implements': [],
        'extends': '',
        'imports': ['java.util.List'],
        'fields': [{'fieldType': 'private int', 'fieldDefinition': 'number;'}],
        'methods': [
            {
                'returnType': 'public void',
                'methodName': 'testMethod',
                'params': [{'paramType': 'String', 'paramName': 'param'}],
                'callMethods': []
            }
        ]
    }
    ast_info = extractor.extract(file_content, methods)
    assert ast_info == expected_ast_info


def test_extract2():
    extractor = JavaExtractor()
    file_content = """/*
    * Copyright (C) 2013-2018 NTT DATA Corporation
    *
    * Licensed under the Apache License, Version 2.0 (the "License");
    * you may not use this file except in compliance with the License.
    * You may obtain a copy of the License at
    *
    *     http://www.apache.org/licenses/LICENSE-2.0
    *
    * Unless required by applicable law or agreed to in writing, software
    * distributed under the License is distributed on an "AS IS" BASIS,
    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
    * either express or implied. See the License for the specific language
    * governing permissions and limitations under the License.
    */
    package org.terasoluna.tourreservation.domain.service.tourinfo;

    import java.util.Collections;
    import java.util.List;

    import javax.inject.Inject;

    import org.springframework.data.domain.Page;
    import org.springframework.data.domain.PageImpl;
    import org.springframework.data.domain.Pageable;
    import org.springframework.stereotype.Service;
    import org.springframework.transaction.annotation.Transactional;
    import org.terasoluna.tourreservation.domain.model.TourInfo;
    import org.terasoluna.tourreservation.domain.repository.tourinfo.TourInfoRepository;
    import org.terasoluna.tourreservation.domain.repository.tourinfo.TourInfoSearchCriteria;

    /**
    * Service for search tour information.
    */
    @Service
    @Transactional
    public class TourInfoServiceImpl implements TourInfoService {

        @Inject
        TourInfoRepository tourInfoRepository;

        @Override
        public Page<TourInfo> searchTour(TourInfoSearchCriteria criteria,
                Pageable pageable) {

            long total = tourInfoRepository.countBySearchCriteria(criteria);
            List<TourInfo> content;
            if (0 < total) {
                content = tourInfoRepository.findPageBySearchCriteria(criteria,
                        pageable);
            } else {
                content = Collections.emptyList();
            }

            Page<TourInfo> page = new PageImpl<TourInfo>(content, pageable, total);
            return page;
        }
    }
    """
    methods = ["testMethod"]
    expected_ast_info = {
    }
    ast_info = extractor.extract(file_content, methods)
    assert ast_info == expected_ast_info

class TestListener:
    def test_extract_java_method(self):
        file_content = """package com.example.sample;

import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;
import lombok.AllArgsConstructor;

@Service
@AllArgsConstructor
public class SampleService {
  private SampleRepository sampleRepository;

  public List<SampleItem> getExistItems(List<Long> ids) {
    return this.sampleRepository.findByItemIdIn(ids);
  }

  public boolean existAll(List<Long> ids) {
    List<CatalogItem> items = this.sampleRepository.findByIdIn(ids);
    List<Long> notExistIds = ids.stream()
        .filter(itemId -> !this.existItemIdInItems(items, itemId))
        .collect(Collectors.toList());

    return notExistIds.isEmpty();
  }

  private boolean existItemIdInItems(List<SampleItem> items, long id) {
    return items.stream().anyMatch(item -> item.getId() == id);
  }
}
"""
        methods = ["getExistItems"]
        expected = """package com.example.sample;

import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;
import lombok.AllArgsConstructor;

@Service
@AllArgsConstructor
public class SampleService {
  private SampleRepository sampleRepository;

  public List<SampleItem> getExistItems(List<Long> ids) {
    return this.sampleRepository.findByItemIdIn(ids);
  }
}
"""

        extractor = JavaExtractor()
        actual = extractor.extract(file_content, methods)
        assert actual == expected

from pytest import mark
from unittest.mock import patch

import src.logger
from .java_extractor import JavaExtractor


class TestJavaExtractor:
    @mark.parametrize(['file_content', 'expected_methods', 'package_name', 'class_name'], [
        (
            """package com.example.sample;

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

  @Override
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
""",
            ["getExistItems", "existAll", "existItemIdInItems"],
            "com.example.sample",
            "SampleService",
        ),
        (
                """package com.example.sample;

import lombok.Data;

@Data
public class Item {
    private long id;
    private String name;
}
""",
                [],
                "com.example.sample",
                "Item",
        )
    ])
    def test_extract_method_names(self, file_content, expected_methods, package_name, class_name):
        if len(expected_methods) > 0:
            expected = (
                [],
                [
                    package_name + '.' + class_name + '#' + method_name
                    for method_name in expected_methods
                ]
            )
        else:
            expected = (
                [
                    package_name + '.' + class_name
                ],
                []
            )

        extractor = JavaExtractor()
        actual = extractor.extract_class_method_names(file_content)
        assert actual == expected

    @patch.object(src.logger.Logger, '__init__', return_value=None)
    @patch.object(src.logger.Logger, 'error', return_value=None)
    @mark.parametrize('file_content, methods, expected', [
        (
            """package com.example;
import java.util.List;
public class TestClass {
    private int number;
    public void testMethod(String param) {
        List<String> list = new ArrayList<>();
        list.add(param);
        System.out.println(list);
    }
}
""",
            ["testMethod"],
            """package com.example;
import java.util.List;
public class TestClass {
    private int number;
    public void testMethod(String param) {
        List<String> list = new ArrayList<>();
        list.add(param);
        System.out.println(list);
    }
}
""",
        ),
        (
            """package com.example.sample;

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

  @Override
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
""",
            ['getExistItems'],
            """package com.example.sample;

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
        ),
        (
            """package com.example.sample;

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

  @Override
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
""",
            ['getExistItems', 'existAll'],
            """package com.example.sample;

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

  @Override
  public boolean existAll(List<Long> ids) {
    List<CatalogItem> items = this.sampleRepository.findByIdIn(ids);
    List<Long> notExistIds = ids.stream()
        .filter(itemId -> !this.existItemIdInItems(items, itemId))
        .collect(Collectors.toList());

    return notExistIds.isEmpty();
  }
}
"""
        ),
        (
             """package com.example.sample;

import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;
import lombok.AllArgsConstructor;

/**
 * The SampleService class is a service layer in the application that handles business logic related to SampleItems.
 * It uses the SampleRepository to interact with the underlying data store.
 *
 * It provides methods to:
 * - Get existing items from the repository by their IDs.
 * - Check if all the items identified by the given IDs exist in the repository.
 * - Check if a given item ID exists in the provided list of items.
 *
 * @Service This annotation is a specialized form of the component annotation which allows us
 * to auto-detect implementation classes through classpath scanning.
 * @AllArgsConstructor This annotation from the Lombok library generates a constructor with a parameter
 * for each field in the class.
 */
@Service
@AllArgsConstructor
public class SampleService {
  private SampleRepository sampleRepository;
  
  /**
   * This method is used to get the existing items from the repository by their IDs.
   *
   * @param ids A list of item IDs to be searched in the repository.
   * @return A list of SampleItem objects that exist in the repository.
   */
  public List<SampleItem> getExistItems(List<Long> ids) {
    return this.sampleRepository.findByItemIdIn(ids);
  }

  /**
   * This method checks if all the items identified by the given IDs exist in the repository.
   *
   * It first retrieves the items from the repository using the provided IDs. Then, it creates a list of IDs
   * that do not exist in the retrieved items.
   * If the list of non-existing IDs is empty, it means all the items exist in the repository,
   * and the method returns true. Otherwise, it returns false.
   *
   * @param ids A list of item IDs to be checked in the repository.
   * @return A boolean indicating whether all the items exist in the repository.
   */
  @Override
  public boolean existAll(List<Long> ids) {
    List<CatalogItem> items = this.sampleRepository.findByIdIn(ids);
    List<Long> notExistIds = ids.stream()
        .filter(itemId -> !this.existItemIdInItems(items, itemId))
        .collect(Collectors.toList());

    return notExistIds.isEmpty();
  }

  /**
   * This method checks if a given item ID exists in the provided list of items.
   *
   * It iterates over the list of items and checks if any item's ID matches the provided ID.
   * If a match is found, it returns true, indicating that the item exists in the list. Otherwise, it returns false.
   *
   * @param items A list of SampleItem objects.
   * @param id The ID of the item to be checked.
   * @return A boolean indicating whether the item exists in the list.
   */
  private boolean existItemIdInItems(List<SampleItem> items, long id) {
    return items.stream().anyMatch(item -> item.getId() == id);
  }
}
""",
             ['existAll'],
             """package com.example.sample;

import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;
import lombok.AllArgsConstructor;

/**
 * The SampleService class is a service layer in the application that handles business logic related to SampleItems.
 * It uses the SampleRepository to interact with the underlying data store.
 *
 * It provides methods to:
 * - Get existing items from the repository by their IDs.
 * - Check if all the items identified by the given IDs exist in the repository.
 * - Check if a given item ID exists in the provided list of items.
 *
 * @Service This annotation is a specialized form of the component annotation which allows us
 * to auto-detect implementation classes through classpath scanning.
 * @AllArgsConstructor This annotation from the Lombok library generates a constructor with a parameter
 * for each field in the class.
 */
@Service
@AllArgsConstructor
public class SampleService {
  private SampleRepository sampleRepository;

  /**
   * This method checks if all the items identified by the given IDs exist in the repository.
   *
   * It first retrieves the items from the repository using the provided IDs. Then, it creates a list of IDs
   * that do not exist in the retrieved items.
   * If the list of non-existing IDs is empty, it means all the items exist in the repository,
   * and the method returns true. Otherwise, it returns false.
   *
   * @param ids A list of item IDs to be checked in the repository.
   * @return A boolean indicating whether all the items exist in the repository.
   */
  @Override
  public boolean existAll(List<Long> ids) {
    List<CatalogItem> items = this.sampleRepository.findByIdIn(ids);
    List<Long> notExistIds = ids.stream()
        .filter(itemId -> !this.existItemIdInItems(items, itemId))
        .collect(Collectors.toList());

    return notExistIds.isEmpty();
  }
}
""",
             ),
        ]
    )
    def test_extract_target_methods(self, _mock_logger, _mock_logger_error, file_content, methods, expected):
        extractor = JavaExtractor()
        actual = extractor.extract_methods(file_content, methods)
        assert actual == expected
